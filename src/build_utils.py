import subprocess
import os

def build_project(project_dir, build_dir):
    os.makedirs(build_dir, exist_ok=True)
    cmake_cmd = ["cmake", project_dir]
    make_cmd = ["cmake", "--build", "."]
    try:
        subprocess.run(cmake_cmd, cwd=build_dir, check=True, capture_output=True)
        result = subprocess.run(make_cmd, cwd=build_dir, check=True, capture_output=True)
        return True, result.stdout.decode()
    except subprocess.CalledProcessError as e:
        return False, e.stderr.decode()

def run_tests(build_dir):
    test_cmd = ["ctest", "--output-on-failure"]
    result = subprocess.run(test_cmd, cwd=build_dir, capture_output=True)
    return result.returncode == 0, result.stdout.decode() + result.stderr.decode()

def run_coverage(build_dir):
    # Example for gcov/lcov; adjust as needed for your setup
    coverage_cmd = ["lcov", "--capture", "--directory", ".", "--output-file", "coverage.info"]
    subprocess.run(coverage_cmd, cwd=build_dir)
    genhtml_cmd = ["genhtml", "coverage.info", "--output-directory", "coverage"]
    subprocess.run(genhtml_cmd, cwd=build_dir)
    return os.path.join(build_dir, "coverage/index.html")