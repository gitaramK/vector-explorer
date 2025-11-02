import * as vscode from 'vscode';
import { getNonce } from '../utils/getNonce';

export class VectorExplorerSidebarProvider implements vscode.WebviewViewProvider {
    public static readonly viewType = 'vectorExplorerSidebar';
    
    private _view?: vscode.WebviewView;

    constructor(
        private readonly _extensionUri: vscode.Uri,
        private readonly _context: vscode.ExtensionContext
    ) {}

    public resolveWebviewView(
        webviewView: vscode.WebviewView,
        context: vscode.WebviewViewResolveContext,
        _token: vscode.CancellationToken
    ) {
        this._view = webviewView;

        webviewView.webview.options = {
            enableScripts: true,
            localResourceRoots: [
                vscode.Uri.joinPath(this._extensionUri, 'media')
            ]
        };

        webviewView.webview.html = this._getHtmlContent(webviewView.webview);

        // Handle messages from webview
        webviewView.webview.onDidReceiveMessage(async (message) => {
            switch (message.type) {
                case 'openDatabase':
                    // Trigger the command which will open in right panel
                    await vscode.commands.executeCommand('vectorExplorer.openVectorDB');
                    break;
            }
        });
    }

    private _getHtmlContent(webview: vscode.Webview): string {
        const styleUri = webview.asWebviewUri(
            vscode.Uri.joinPath(this._extensionUri, 'media', 'sidebar.css')
        );

        const nonce = getNonce();

        return `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src ${webview.cspSource} 'unsafe-inline'; script-src 'nonce-${nonce}';">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="${styleUri}" rel="stylesheet">
    <title>Vector Explorer</title>
</head>
<body>
    <div class="sidebar-container">
        <div class="sidebar-header">
            <div class="sidebar-icon">📊</div>
            <h2>Vector Explorer</h2>
            <p class="sidebar-description">Explore and visualize your vector databases</p>
        </div>

        <div class="sidebar-content">
            <button id="open-db-btn" class="btn-primary">
                📂 Open Vector Database
            </button>
            
            <div class="sidebar-info">
                <h3>Supported Formats:</h3>
                <ul>
                    <li>✓ FAISS (.faiss, index.faiss)</li>
                    <li>✓ Chroma (folder with chroma.sqlite3)</li>
                </ul>
            </div>

            <div class="sidebar-features">
                <h3>Features:</h3>
                <ul>
                    <li>🔍 Search and filter vectors</li>
                    <li>📊 View embeddings and text chunks</li>
                    <li>📥 Export to CSV</li>
                    <li>🔢 Copy vectors and text</li>
                </ul>
            </div>
        </div>
    </div>

    <script nonce="${nonce}">
        const vscode = acquireVsCodeApi();
        
        document.getElementById('open-db-btn').addEventListener('click', () => {
            vscode.postMessage({ type: 'openDatabase' });
        });
    </script>
</body>
</html>`;
    }
}
