import os
import sys
from llm_client import call_llm
from build_utils import build_project, run_tests, run_coverage

def read_file(path):
    with open(path, "r") as f:
        return f.read()

def write_file(path, content):
    with open(path, "w") as f:
        f.write(content)

def collect_cpp_files(project_dir):
    cpp_files = []
    for root, dirs, files in os.walk(project_dir):
        # Skip third_party directory to avoid processing external libraries
        if "third_party" in root:
            continue
        for file in files:
            if file.endswith(".cc") or file.endswith(".cpp"):
                cpp_files.append(os.path.join(root, file))
    return cpp_files

def main():
    # Get the directory where main.py is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    
    project_dir = os.path.join(project_root, "test_projects", "orgChartApi-master")
    test_dir = os.path.join(project_root, "generated_tests")
    build_dir = os.path.join(project_root, "build")
    yaml_dir = os.path.join(script_dir, "yaml_prompts")
    
    os.makedirs(test_dir, exist_ok=True)

    print("🚀 Starting C++ Unit Test Generation Pipeline")
    print(f"📁 Project directory: {project_dir}")
    print(f"📁 Test directory: {test_dir}")
    print(f"📁 Build directory: {build_dir}")

    # 1. Initial test generation
    print("\n📝 Step 1: Generating initial unit tests...")
    cpp_files = collect_cpp_files(project_dir)
    print(f"Found {len(cpp_files)} C++ files to process:")
    for cpp_file in cpp_files:
        print(f"  - {cpp_file}")
    
    for cpp_file in cpp_files:
        try:
            print(f"\nProcessing: {cpp_file}")
            code = read_file(cpp_file)
            yaml_prompt = read_file(os.path.join(yaml_dir, "initial.yaml"))
            prompt = f"{yaml_prompt}\n\nC++ Source File:\n{code}"
            test_code = call_llm(prompt)
            test_file = os.path.join(test_dir, f"test_{os.path.basename(cpp_file)}")
            write_file(test_file, test_code)
            print(f"✅ Generated test: {test_file}")
        except Exception as e:
            print(f"❌ Error processing {cpp_file}: {e}")
            continue

    # 2. Refine tests
    print("\n🔧 Step 2: Refining generated tests...")
    test_files = [f for f in os.listdir(test_dir) if f.endswith('.cc') or f.endswith('.cpp')]
    print(f"Found {len(test_files)} test files to refine:")
    for test_file in test_files:
        print(f"  - {test_file}")
    
    for test_file in test_files:
        try:
            print(f"\nRefining: {test_file}")
            test_path = os.path.join(test_dir, test_file)
            test_code = read_file(test_path)
            yaml_prompt = read_file(os.path.join(yaml_dir, "refine.yaml"))
            prompt = f"{yaml_prompt}\n\nTest File:\n{test_code}"
            refined_code = call_llm(prompt)
            write_file(test_path, refined_code)
            print(f"✅ Refined test: {test_file}")
        except Exception as e:
            print(f"❌ Error refining {test_file}: {e}")
            continue

    # 3. Build and debug
    print("\n🔨 Step 3: Building project with generated tests...")
    build_success, build_log = build_project(project_dir, build_dir)
    if not build_success:
        print("❌ Build failed. Attempting to fix issues...")
        print(f"Build log:\n{build_log}")
        try:
            yaml_prompt = read_file(os.path.join(yaml_dir, "fix_build.yaml"))
            prompt = f"{yaml_prompt}\n\nBuild Log:\n{build_log}"
            fixed_code = call_llm(prompt)
            print("🔧 LLM provided fix suggestions. Manual review may be needed.")
        except Exception as e:
            print(f"❌ Error during build fix attempt: {e}")
    else:
        print("✅ Build successful!")
        
        # 4. Run tests and coverage
        print("\n🧪 Step 4: Running tests and generating coverage...")
        test_success, test_log = run_tests(build_dir)
        if test_success:
            print("✅ Tests passed!")
            try:
                coverage_report = run_coverage(build_dir)
                print(f"📊 Coverage report generated at: {coverage_report}")
            except Exception as e:
                print(f"❌ Error generating coverage: {e}")
        else:
            print("❌ Tests failed!")
            print(f"Test log:\n{test_log}")
    
    print("\n🎉 Pipeline completed!")

if __name__ == "__main__":
    main()