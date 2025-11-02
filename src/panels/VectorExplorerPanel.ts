import * as vscode from 'vscode';
import * as path from 'path';
import { VectorDBLoader } from '../services/VectorDBLoader';
import { VectorData } from '../types';
import { getNonce } from '../utils/getNonce';

export class VectorExplorerPanel {
    public static currentPanel: VectorExplorerPanel | undefined;
    private readonly _panel: vscode.WebviewPanel;
    private readonly _extensionUri: vscode.Uri;
    private readonly _context: vscode.ExtensionContext;
    private _disposables: vscode.Disposable[] = [];
    private _currentData: VectorData | undefined;
    private _loader: VectorDBLoader;
    private _isDisposed: boolean = false;

    constructor(extensionUri: vscode.Uri, context: vscode.ExtensionContext) {
        this._extensionUri = extensionUri;
        this._context = context;
        this._loader = new VectorDBLoader(context);

        // Create webview panel
        this._panel = vscode.window.createWebviewPanel(
            'vectorExplorer',
            'Vector Explorer',
            vscode.ViewColumn.Two,
            {
                enableScripts: true,
                localResourceRoots: [
                    vscode.Uri.joinPath(this._extensionUri, 'media'),
                    vscode.Uri.joinPath(this._extensionUri, 'dist')
                ],
                retainContextWhenHidden: true
            }
        );

        // Set the HTML content
        this._panel.webview.html = this._getHtmlContent(this._panel.webview);

        // Handle messages from webview
        this._panel.webview.onDidReceiveMessage(
            async (message) => {
                switch (message.type) {
                    case 'refresh':
                        if (this._currentData) {
                            this._panel.webview.postMessage({
                                type: 'vectorData',
                                data: this._currentData
                            });
                        }
                        break;
                    case 'copyVector':
                        await vscode.env.clipboard.writeText(JSON.stringify(message.vector));
                        vscode.window.showInformationMessage('Vector copied to clipboard');
                        break;
                    case 'copyText':
                        await vscode.env.clipboard.writeText(message.text);
                        vscode.window.showInformationMessage('Text copied to clipboard');
                        break;
                    case 'export':
                        await vscode.commands.executeCommand('vectorExplorer.exportCSV');
                        break;
                    case 'error':
                        vscode.window.showErrorMessage(message.message);
                        break;
                }
            },
            null,
            this._disposables
        );

        // Handle panel disposal
        this._panel.onDidDispose(() => this.dispose(), null, this._disposables);
    }

    public async loadVectorDB(dbPath: string) {
        try {
            vscode.window.withProgress(
                {
                    location: vscode.ProgressLocation.Notification,
                    title: 'Loading Vector Database...',
                    cancellable: false
                },
                async (progress) => {
                    progress.report({ message: 'Detecting database type...' });
                    
                    const data = await this._loader.loadVectorDB(dbPath);
                    this._currentData = data;

                    progress.report({ message: 'Rendering data...' });
                    
                    // Send data to webview
                    this._panel.webview.postMessage({
                        type: 'vectorData',
                        data: data
                    });

                    vscode.window.showInformationMessage(
                        `Loaded ${data.count} vectors from ${data.type.toUpperCase()} database`
                    );
                }
            );
        } catch (error) {
            vscode.window.showErrorMessage(
                `Failed to load vector database: ${error instanceof Error ? error.message : String(error)}`
            );
        }
    }

    public reveal() {
        if (!this._isDisposed) {
            this._panel.reveal(vscode.ViewColumn.Two);
        }
    }

    public refresh() {
        if (this._currentData && !this._isDisposed) {
            this._panel.webview.postMessage({
                type: 'vectorData',
                data: this._currentData
            });
        }
    }

    public isDisposed(): boolean {
        return this._isDisposed;
    }

    public dispose() {
        this._isDisposed = true;
        this._panel.dispose();
        while (this._disposables.length) {
            const disposable = this._disposables.pop();
            if (disposable) {
                disposable.dispose();
            }
        }
    }

    public onDispose(callback: () => void) {
        this._panel.onDidDispose(callback, null, this._disposables);
    }

    public async getCurrentData(): Promise<VectorData | undefined> {
        return this._currentData;
    }

    private _getHtmlContent(webview: vscode.Webview): string {
        const styleUri = webview.asWebviewUri(
            vscode.Uri.joinPath(this._extensionUri, 'media', 'main.css')
        );
        const scriptUri = webview.asWebviewUri(
            vscode.Uri.joinPath(this._extensionUri, 'media', 'main.js')
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
    <div id="app">
        <div class="header">
            <h1>🔍 Vector Explorer</h1>
            <div class="header-info">
                <span id="db-type" class="badge">Type: -</span>
                <span id="db-count" class="badge">Count: 0</span>
                <span id="db-dimension" class="badge">Dimension: 0</span>
            </div>
        </div>

        <div class="toolbar">
            <input type="text" id="search-box" placeholder="🔎 Search by ID or text..." class="search-input">
            <button id="refresh-btn" class="btn">🔄 Refresh</button>
            <button id="export-btn" class="btn">📥 Export CSV</button>
        </div>

        <div class="content">
            <div class="table-container">
                <div id="loading" class="loading">
                    <div class="spinner"></div>
                    <p>Loading vector database...</p>
                </div>
                <div id="error" class="error-message" style="display: none;"></div>
                <table id="vector-table" class="vector-table" style="display: none;">
                    <thead>
                        <tr>
                            <th class="sortable" data-column="id">ID <span class="sort-icon">↕</span></th>
                            <th class="sortable" data-column="text">Text Chunk <span class="sort-icon">↕</span></th>
                            <th>Vector (first 5)</th>
                            <th class="sortable" data-column="source">Source <span class="sort-icon">↕</span></th>
                        </tr>
                    </thead>
                    <tbody id="table-body">
                    </tbody>
                </table>
            </div>

            <div class="pagination">
                <button id="prev-page" class="btn-pagination" disabled>← Previous</button>
                <span id="page-info">Page 1 of 1</span>
                <button id="next-page" class="btn-pagination" disabled>Next →</button>
            </div>
        </div>
    </div>

    <!-- Modal for full text -->
    <div id="text-modal" class="modal">
        <div class="modal-content">
            <div class="modal-header">
                <h2>Full Text Chunk</h2>
                <button class="close-btn" id="close-modal">&times;</button>
            </div>
            <div class="modal-body">
                <div class="modal-metadata">
                    <div><strong>ID:</strong> <span id="modal-id"></span></div>
                    <div><strong>Source:</strong> <span id="modal-source"></span></div>
                    <div><strong>Length:</strong> <span id="modal-length"></span> characters</div>
                </div>
                <div class="modal-text" id="modal-text"></div>
            </div>
            <div class="modal-footer">
                <button id="copy-text-btn" class="btn">📋 Copy Text</button>
            </div>
        </div>
    </div>

    <!-- Modal for full vector -->
    <div id="vector-modal" class="modal">
        <div class="modal-content">
            <div class="modal-header">
                <h2>Full Vector</h2>
                <button class="close-btn" id="close-vector-modal">&times;</button>
            </div>
            <div class="modal-body">
                <div class="modal-metadata">
                    <div><strong>ID:</strong> <span id="vector-modal-id"></span></div>
                    <div><strong>Dimensions:</strong> <span id="vector-dimensions"></span></div>
                </div>
                <pre class="vector-display" id="vector-display"></pre>
            </div>
            <div class="modal-footer">
                <button id="copy-vector-btn" class="btn">📋 Copy Vector</button>
            </div>
        </div>
    </div>

    <script nonce="${nonce}" src="${scriptUri}"></script>
</body>
</html>`;
    }
}
