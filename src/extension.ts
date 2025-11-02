import * as vscode from 'vscode';
import { VectorExplorerPanel } from './panels/VectorExplorerPanel';
import { VectorExplorerSidebarProvider } from './providers/VectorExplorerSidebarProvider';
import { exportToCSV } from './utils/csvExporter';

let currentPanel: VectorExplorerPanel | undefined;
let sidebarProvider: VectorExplorerSidebarProvider;

export function activate(context: vscode.ExtensionContext) {
    console.log('Vector Explorer extension activated');

    // Register sidebar provider
    sidebarProvider = new VectorExplorerSidebarProvider(context.extensionUri, context);
    
    context.subscriptions.push(
        vscode.window.registerWebviewViewProvider(
            VectorExplorerSidebarProvider.viewType,
            sidebarProvider
        )
    );

    // Register "Open Vector DB" command - Opens in right panel
    const openVectorDBCommand = vscode.commands.registerCommand(
        'vectorExplorer.openVectorDB',
        async (uri?: vscode.Uri) => {
            try {
                let selectedPath: string | undefined;

                if (uri) {
                    selectedPath = uri.fsPath;
                } else {
                    // Show file picker dialog
                    const options: vscode.OpenDialogOptions = {
                        canSelectFiles: true,
                        canSelectFolders: true,
                        canSelectMany: false,
                        openLabel: 'Open Vector Database',
                        filters: {
                            'Vector DB': ['faiss', 'index'],
                            'All Files': ['*']
                        }
                    };

                    const fileUri = await vscode.window.showOpenDialog(options);
                    if (fileUri && fileUri[0]) {
                        selectedPath = fileUri[0].fsPath;
                    }
                }

                if (!selectedPath) {
                    return;
                }

                // Create or show the panel on the right
                // Check if panel exists and is not disposed
                if (currentPanel && !currentPanel.isDisposed()) {
                    currentPanel.reveal();
                    await currentPanel.loadVectorDB(selectedPath);
                } else {
                    // Create new panel if it doesn't exist or is disposed
                    currentPanel = new VectorExplorerPanel(context.extensionUri, context);
                    await currentPanel.loadVectorDB(selectedPath);

                    // Reset when panel is closed
                    currentPanel.onDispose(() => {
                        currentPanel = undefined;
                    });
                }
            } catch (error) {
                vscode.window.showErrorMessage(
                    `Failed to open vector database: ${error instanceof Error ? error.message : String(error)}`
                );
            }
        }
    );

    // Register "Refresh" command
    const refreshCommand = vscode.commands.registerCommand(
        'vectorExplorer.refresh',
        () => {
            if (currentPanel) {
                currentPanel.refresh();
            }
        }
    );

    // Register "Export CSV" command
    const exportCSVCommand = vscode.commands.registerCommand(
        'vectorExplorer.exportCSV',
        async () => {
            const data = await currentPanel?.getCurrentData();
            
            if (!data || !data.vectors || data.vectors.length === 0) {
                vscode.window.showWarningMessage('No data to export');
                return;
            }

            try {
                await exportToCSV(data);
                vscode.window.showInformationMessage('Vector data exported successfully');
            } catch (error) {
                vscode.window.showErrorMessage(
                    `Failed to export CSV: ${error instanceof Error ? error.message : String(error)}`
                );
            }
        }
    );

    context.subscriptions.push(openVectorDBCommand, refreshCommand, exportCSVCommand);
}

export function deactivate() {
    if (currentPanel) {
        currentPanel.dispose();
    }
}
