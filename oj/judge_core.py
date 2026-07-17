# judge_core.py
# 判题核心接口 - 支持代码编译、运行和测试
# 适用于 Windows 8.1，单个文件，可通过HTTP调用

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import subprocess
import tempfile
import os
import shutil
import time
import threading
import urllib.parse

class JudgeCore:
    """判题核心类"""
    
    def __init__(self):
        self.supported_languages = {
            'python': {
                'ext': '.py',
                'compile_cmd': None,
                'run_cmd': ['python', '{code_file}'],
                'timeout': 5
            },
            'cpp': {
                'ext': '.cpp',
                'compile_cmd': ['g++', '{code_file}', '-o', '{exe_file}'],
                'run_cmd': ['{exe_file}'],
                'timeout': 3
            },
            'c': {
                'ext': '.c',
                'compile_cmd': ['gcc', '{code_file}', '-o', '{exe_file}'],
                'run_cmd': ['{exe_file}'],
                'timeout': 3
            },
            'java': {
                'ext': '.java',
                'compile_cmd': ['javac', '{code_file}'],
                'run_cmd': ['java', '-cp', '{work_dir}', '{class_name}'],
                'timeout': 5
            },
            'javascript': {
                'ext': '.js',
                'compile_cmd': None,
                'run_cmd': ['node', '{code_file}'],
                'timeout': 5
            }
        }
    
    def judge(self, code, language, test_cases, time_limit=None):
        """
        判题主函数
        :param code: 源代码字符串
        :param language: 编程语言
        :param test_cases: 测试用例列表 [{'input': '...', 'output': '...'}, ...]
        :param time_limit: 时间限制（秒）
        :return: 判题结果
        """
        if language not in self.supported_languages:
            return {
                'status': 'error',
                'message': f'不支持的语言: {language}',
                'supported': list(self.supported_languages.keys())
            }
        
        # 创建临时工作目录
        work_dir = tempfile.mkdtemp(prefix='judge_')
        
        try:
            # 准备代码文件
            lang_config = self.supported_languages[language]
            code_file = os.path.join(work_dir, f'code{lang_config["ext"]}')
            
            with open(code_file, 'w', encoding='utf-8') as f:
                f.write(code)
            
            # 编译（如果需要）
            if lang_config['compile_cmd']:
                compile_result = self._compile(code_file, work_dir, lang_config)
                if compile_result['status'] == 'error':
                    return compile_result
            
            # 运行测试用例
            results = []
            passed = 0
            total = len(test_cases)
            
            for i, test_case in enumerate(test_cases):
                test_result = self._run_test(
                    code_file, 
                    work_dir, 
                    lang_config, 
                    test_case,
                    time_limit or lang_config['timeout']
                )
                results.append(test_result)
                if test_result['status'] == 'passed':
                    passed += 1
            
            return {
                'status': 'success',
                'passed': passed,
                'total': total,
                'results': results,
                'score': f"{passed}/{total}"
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }
        finally:
            # 清理临时目录
            try:
                shutil.rmtree(work_dir)
            except:
                pass
    
    def _compile(self, code_file, work_dir, lang_config):
        """编译代码"""
        exe_file = os.path.join(work_dir, 'program')
        compile_cmd = [cmd.replace('{code_file}', code_file).replace('{exe_file}', exe_file) 
                      for cmd in lang_config['compile_cmd']]
        
        try:
            result = subprocess.run(
                compile_cmd,
                cwd=work_dir,
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode != 0:
                return {
                    'status': 'error',
                    'message': '编译错误',
                    'detail': result.stderr or result.stdout
                }
            
            return {'status': 'success'}
            
        except subprocess.TimeoutExpired:
            return {
                'status': 'error',
                'message': '编译超时'
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': f'编译异常: {str(e)}'
            }
    
    def _run_test(self, code_file, work_dir, lang_config, test_case, timeout):
        """运行单个测试用例"""
        # 准备运行命令
        exe_file = os.path.join(work_dir, 'program')
        class_name = os.path.splitext(os.path.basename(code_file))[0]
        
        run_cmd = []
        for cmd in lang_config['run_cmd']:
            cmd = cmd.replace('{code_file}', code_file)
            cmd = cmd.replace('{exe_file}', exe_file)
            cmd = cmd.replace('{work_dir}', work_dir)
            cmd = cmd.replace('{class_name}', class_name)
            run_cmd.append(cmd)
        
        start_time = time.time()
        
        try:
            # 运行程序
            process = subprocess.Popen(
                run_cmd,
                cwd=work_dir,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # 输入数据并获取输出
            try:
                stdout, stderr = process.communicate(
                    input=test_case.get('input', ''),
                    timeout=timeout
                )
            except subprocess.TimeoutExpired:
                process.kill()
                return {
                    'status': 'timeout',
                    'message': '运行超时',
                    'input': test_case.get('input', ''),
                    'expected': test_case.get('output', ''),
                    'actual': ''
                }
            
            elapsed_time = time.time() - start_time
            actual_output = stdout.strip()
            expected_output = test_case.get('output', '').strip()
            
            # 判断结果
            if process.returncode != 0:
                return {
                    'status': 'runtime_error',
                    'message': '运行时错误',
                    'stderr': stderr,
                    'input': test_case.get('input', ''),
                    'expected': expected_output,
                    'actual': actual_output
                }
            
            # 比较输出（忽略末尾换行和空格差异）
            if self._compare_output(actual_output, expected_output):
                return {
                    'status': 'passed',
                    'message': '通过',
                    'input': test_case.get('input', ''),
                    'expected': expected_output,
                    'actual': actual_output,
                    'time': f'{elapsed_time:.3f}s'
                }
            else:
                return {
                    'status': 'failed',
                    'message': '答案错误',
                    'input': test_case.get('input', ''),
                    'expected': expected_output,
                    'actual': actual_output,
                    'time': f'{elapsed_time:.3f}s'
                }
                
        except Exception as e:
            return {
                'status': 'error',
                'message': f'运行异常: {str(e)}',
                'input': test_case.get('input', ''),
                'expected': test_case.get('output', ''),
                'actual': ''
            }
    
    def _compare_output(self, actual, expected):
        """比较输出结果"""
        # 按行比较，忽略末尾空格
        actual_lines = [line.rstrip() for line in actual.split('\n') if line.rstrip()]
        expected_lines = [line.rstrip() for line in expected.split('\n') if line.rstrip()]
        
        if len(actual_lines) != len(expected_lines):
            return False
        
        for a, e in zip(actual_lines, expected_lines):
            if a != e:
                return False
        
        return True


class JudgeHandler(BaseHTTPRequestHandler):
    """HTTP请求处理器"""
    
    judge_core = JudgeCore()
    
    def do_OPTIONS(self):
        """处理CORS预检请求"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_POST(self):
        """处理POST请求"""
        if self.path == '/judge':
            self._handle_judge()
        elif self.path == '/languages':
            self._handle_languages()
        else:
            self._send_error(404, 'Not Found')
    
    def do_GET(self):
        """处理GET请求"""
        if self.path == '/':
            self._send_html_form()
        elif self.path == '/languages':
            self._handle_languages()
        else:
            self._send_error(404, 'Not Found')
    
    def _handle_judge(self):
        """处理判题请求"""
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            # 验证必需参数
            required = ['code', 'language', 'test_cases']
            for field in required:
                if field not in data:
                    self._send_error(400, f'缺少必需参数: {field}')
                    return
            
            # 执行判题
            result = self.judge_core.judge(
                code=data['code'],
                language=data['language'],
                test_cases=data['test_cases'],
                time_limit=data.get('time_limit')
            )
            
            self._send_json(result)
            
        except json.JSONDecodeError:
            self._send_error(400, 'Invalid JSON')
        except Exception as e:
            self._send_error(500, str(e))
    
    def _handle_languages(self):
        """获取支持的语言列表"""
        self._send_json({
            'languages': list(self.judge_core.supported_languages.keys())
        })
    
    def _send_html_form(self):
        """发送HTML测试界面"""
        html = '''
        <head><meta charset="UTF-8"></head>
        <h1>这是一个小小的接口</h1>
        '''
        self._send_html(html)
    
    def _send_json(self, data):
        """发送JSON响应"""
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))
    
    def _send_html(self, html):
        """发送HTML响应"""
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))
    
    def _send_error(self, code, message):
        """发送错误响应"""
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps({'status': 'error', 'message': message}).encode('utf-8'))
    
    def log_message(self, format, *args):
        """重写日志方法，避免输出过多"""
        pass


def run_server(port=8080):
    """启动服务器"""
    server = HTTPServer(('0.0.0.0', port), JudgeHandler)
    print(f'🚀 判题核心服务已启动')
    print(f'🌐 访问地址: http://localhost:{port}')
    print(f'📝 支持的语言: {list(JudgeHandler.judge_core.supported_languages.keys())}')
    print('按 Ctrl+C 停止服务')
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\n👋 服务已停止')
        server.shutdown()


if __name__ == '__main__':
    run_server()
