import subprocess
import sys
import os

class RunCppCode(object):

    def __init__(self, code=None, code_doc=None):
        self.code = code
        self.code_doc = code_doc
        self.compiler = "g++"
        self.timeLimit = 3
        if not os.path.exists('running'):
            os.mkdir('running')

    def _compile_cpp_code(self, filename, prog="./running/a.out"):
        cmd = [self.compiler, filename, "-Wall", "-o", prog]
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result = p.wait()
        a, b = p.communicate(timeout=self.timeLimit)
        self.stdout, self.stderr = a.decode("utf-8"), b.decode("utf-8")
        return result

    def _run_cpp_prog(self, cmd="./running/a.out"):        
        data, temp = os.pipe()
        os.write(temp, bytes(str(self.code_doc["input"]), "utf-8"))
        os.close(temp)

        # run check output
        s = subprocess.check_output(cmd, stdin = data, shell = True, timeout=self.timeLimit)

        return s.decode("utf-8")

    
    # Compile code
    def compile_cpp_code(self, code=None):
        save_label = False
        id_code = str(self.code_doc["_id"])
        filename = "./running/" + id_code + ".cpp"
        fileout = "./running/" + id_code + ".out"

        if not code:
            code = self.code
        result_run = "No run done"
        try:
            # write code to file
            with open(filename, "w") as f:
                f.write(code)

            #compiler code
            res = self._compile_cpp_code(filename, fileout)
            result_compilation = self.stdout + self.stderr
        finally:
            # delete file
            if os.path.exists(filename):
                os.remove(filename)
            if os.path.exists(fileout):
                os.remove(fileout)

        return res, result_compilation


    # Run code
    def run_cpp_code(self, code=None):
        save_label = False
        id_code = str(self.code_doc["_id"])
        filename = "./running/" + id_code + ".cpp"
        fileout = "./running/" + id_code + ".out"

        if not code:
            code = self.code
        result_run = "No run done"

        try: 
             # write code to file
            with open(filename, "w") as f:
                f.write(code)

            #compiler code
            res = self._compile_cpp_code(filename, fileout)
            result_compilation = self.stdout + self.stderr

            if res == 0:
                result_run = self._run_cpp_prog(fileout)

                result_run_replace = result_run.replace(" ", "").replace("\n", "")
                
                result_run_true = str(self.code_doc["output"]).replace(" ", "").replace("\n", "")

                if str(result_run_replace) == str(result_run_true):                
                    save_label = True
        finally:
            # delete file
            if os.path.exists(filename):
                os.remove(filename)
            if os.path.exists(fileout):
                os.remove(fileout)

        return result_compilation, save_label, result_run