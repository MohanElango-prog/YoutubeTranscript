import subprocess

def upgrade_packages():
    result = subprocess.run(["pip", "list", "--outdated", "--format=freeze"], capture_output=True, text=True)
    packages = [line.split('==')[0] for line in result.stdout.split('\n') if line]
    for package in packages:
        subprocess.run(["pip", "install", "--upgrade", package])

if __name__ == "__main__":
    upgrade_packages()
