# python std library
import sys
import subprocess


def run_rgb_feature_metaflow(flow_filepath: str):
    try:
        # Use the correct Python executable for the system
        python_executable = sys.executable
        
        # Run the script using the subprocess module
        process = subprocess.Popen(
            [python_executable, flow_filepath, "run"],
            stdout=subprocess.PIPE,  # Capture stdout
            stderr=subprocess.PIPE   # Capture stderr
        )
        
        # Wait for the process to complete
        stdout, stderr = process.communicate()
        
        # Check if the process ended successfully
        if process.returncode == 0:
            print("Script executed successfully:")
            print(stdout.decode('utf-8'))
        else:
            print("Script failed with return code", process.returncode)
            print(stderr.decode('utf-8'))
    
    except Exception as e:
        print(f"An error occurred: {e}")
