import subprocess

def pytest_configure(config):
    branch = subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"]).decode().strip()

    print(f"Current branch {branch}")

    subprocess.run(["git", "remote", "add", "original_repo", "https://github.com/SlashAirLearningWebDevelopment/BookReviewProject.git"])

    # fetch original main branch 
    subprocess.check_output(["git", "fetch", "original_repo", "main"])
    
    branch_behind_original_repo_count = int(subprocess.check_output(["git", "rev-list","--right-only", "--count", f"{branch}...original_repo/main"]).decode().strip())

    assert branch_behind_original_repo_count == 0, f"""
            Your repo branch {branch} is behind SlashAirLearningWebDevelopment/BookReviewProject 
            by {branch_behind_original_repo_count} commits

            Fix this by fetching upstream code and pulling it on your local machine. 
            """
