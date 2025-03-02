import * as vscode from 'vscode';

export function activate(context: vscode.ExtensionContext) {
  console.log('Extension "auto-commit-copilot" đã được kích hoạt!');

  // Đăng ký lệnh auto-commit
  let disposable = vscode.commands.registerCommand('auto-commit-copilot.autoCommit', async () => {
    try {
      // Hiển thị thông báo
      vscode.window.showInformationMessage('Đang thực hiện Auto Commit với Copilot...');

      // 1. Mở panel Source Control
      await vscode.commands.executeCommand('workbench.view.scm');
      
      // Chờ một chút để panel Source Control được mở hoàn toàn
      await new Promise(resolve => setTimeout(resolve, 1000));

      // 2. Gọi lệnh Generate Commit Message with Copilot
      await vscode.commands.executeCommand('github.copilot.generateCommitMessage');
      
      // Chờ một chút để Copilot tạo commit message
      await new Promise(resolve => setTimeout(resolve, 3000));

      // 3. Thực hiện commit
      await vscode.commands.executeCommand('git.commit');

      // Hiển thị thông báo hoàn thành
      vscode.window.showInformationMessage('Đã hoàn thành quy trình commit!');
    } catch (error) {
      // Hiển thị thông báo lỗi
      vscode.window.showErrorMessage(`Lỗi: ${error}`);
    }
  });

  context.subscriptions.push(disposable);
}

export function deactivate() {} 