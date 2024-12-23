import pytest
from pathlib import Path
import tempfile
import shutil
import git

@pytest.fixture
def temp_git_repo():
    with tempfile.TemporaryDirectory() as tmpdir:
        repo_path = Path(tmpdir)
        repo = git.Repo.init(repo_path)
        
        # Set up basic git config
        with repo.config_writer() as git_config:
            git_config.set_value('user', 'name', 'Test User')
            git_config.set_value('user', 'email', 'test@example.com')
        
        yield repo_path
        shutil.rmtree(tmpdir) 