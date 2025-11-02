import * as vscode from 'vscode';
import * as path from 'path';
import * as fs from 'fs';
import { spawn } from 'child_process';
import { VectorData } from '../types';

export class VectorDBLoader {
    private _context: vscode.ExtensionContext;
    private _detectedPath: string | null = null; // Store the actual detected file/directory path

    constructor(context: vscode.ExtensionContext) {
        this._context = context;
    }

    public async loadVectorDB(dbPath: string): Promise<VectorData> {
        // Check if path exists
        if (!fs.existsSync(dbPath)) {
            throw new Error(`Path does not exist: ${dbPath}`);
        }

        this._detectedPath = null; // Reset
        const dbType = this.detectDatabaseType(dbPath);
        
        if (!dbType) {
            // Provide more detailed error message
            const stat = fs.statSync(dbPath);
            if (stat.isFile()) {
                const ext = path.extname(dbPath);
                throw new Error(
                    `Unable to detect database type for file: ${path.basename(dbPath)}\n` +
                    `File extension: ${ext || 'none'}\n` +
                    `Expected: .faiss or .index file\n` +
                    `Path: ${dbPath}`
                );
            } else if (stat.isDirectory()) {
                const dirContents = fs.readdirSync(dbPath).slice(0, 10).join(', ');
                throw new Error(
                    `Unable to detect database type for directory: ${path.basename(dbPath)}\n` +
                    `Looking for: chroma.sqlite3, index.faiss, or any .faiss/.index files in subdirectories\n` +
                    `Directory contains: ${dirContents}${fs.readdirSync(dbPath).length > 10 ? '...' : ''}\n` +
                    `Path: ${dbPath}`
                );
            } else {
                throw new Error(`Path is neither a file nor a directory: ${dbPath}`);
            }
        }

        // Use the detected path if we found a file in subdirectory, otherwise use original path
        const actualPath = this._detectedPath || dbPath;
        console.log(`[Vector Explorer] Using path: ${actualPath} (type: ${dbType})`);
        
        return await this.loadWithPython(actualPath, dbType);
    }

    private detectDatabaseType(dbPath: string): 'faiss' | 'chroma' | null {
        try {
            const stat = fs.statSync(dbPath);

            if (stat.isFile()) {
                const lowerPath = dbPath.toLowerCase();
                // Check if it's a FAISS index file
                if (lowerPath.endsWith('.faiss') || lowerPath.endsWith('.index')) {
                    this._detectedPath = dbPath;
                    return 'faiss';
                }
            } else if (stat.isDirectory()) {
                // Check for Chroma database (looks for chroma.sqlite3)
                const chromaDbPath = path.join(dbPath, 'chroma.sqlite3');
                if (fs.existsSync(chromaDbPath)) {
                    this._detectedPath = dbPath;
                    return 'chroma';
                }

                // Check for FAISS files in the current directory
                const faissIndexPath = path.join(dbPath, 'index.faiss');
                if (fs.existsSync(faissIndexPath)) {
                    this._detectedPath = faissIndexPath;
                    return 'faiss';
                }

                // Search for .faiss or .index files in subdirectories (up to 3 levels deep)
                const foundFaiss = this.searchForFaissFiles(dbPath, 0, 3);
                if (foundFaiss) {
                    this._detectedPath = foundFaiss;
                    return 'faiss';
                }

                // Search for Chroma databases in subdirectories
                const foundChroma = this.searchForChromaDB(dbPath, 0, 3);
                if (foundChroma) {
                    this._detectedPath = foundChroma;
                    return 'chroma';
                }
            }

            return null;
        } catch (error) {
            console.error('Error detecting database type:', error);
            return null;
        }
    }

    private searchForFaissFiles(dirPath: string, currentDepth: number, maxDepth: number): string | null {
        if (currentDepth > maxDepth) {
            return null;
        }

        try {
            const entries = fs.readdirSync(dirPath, { withFileTypes: true });

            // First check for FAISS files in current directory
            for (const entry of entries) {
                if (entry.isFile()) {
                    const lowerName = entry.name.toLowerCase();
                    if (lowerName.endsWith('.faiss') || lowerName.endsWith('.index')) {
                        const fullPath = path.join(dirPath, entry.name);
                        console.log(`[Vector Explorer] Found FAISS file: ${fullPath}`);
                        return fullPath;
                    }
                }
            }

            // Then check subdirectories (including those starting with .)
            for (const entry of entries) {
                if (entry.isDirectory() && entry.name !== '.' && entry.name !== '..' && entry.name !== '.git') {
                    const subDirPath = path.join(dirPath, entry.name);
                    const found = this.searchForFaissFiles(subDirPath, currentDepth + 1, maxDepth);
                    if (found) {
                        return found;
                    }
                }
            }
        } catch (error) {
            console.error(`Error searching directory ${dirPath}:`, error);
        }

        return null;
    }

    private searchForChromaDB(dirPath: string, currentDepth: number, maxDepth: number): string | null {
        if (currentDepth > maxDepth) {
            return null;
        }

        try {
            const entries = fs.readdirSync(dirPath, { withFileTypes: true });

            // Check for chroma.sqlite3 in current directory
            for (const entry of entries) {
                if (entry.isFile() && entry.name === 'chroma.sqlite3') {
                    console.log(`[Vector Explorer] Found Chroma DB: ${dirPath}`);
                    return dirPath;
                }
            }

            // Check subdirectories (including those starting with .)
            for (const entry of entries) {
                if (entry.isDirectory() && entry.name !== '.' && entry.name !== '..' && entry.name !== '.git') {
                    const subDirPath = path.join(dirPath, entry.name);
                    const found = this.searchForChromaDB(subDirPath, currentDepth + 1, maxDepth);
                    if (found) {
                        return found;
                    }
                }
            }
        } catch (error) {
            console.error(`Error searching directory ${dirPath}:`, error);
        }

        return null;
    }

    private async loadWithPython(dbPath: string, dbType: 'faiss' | 'chroma'): Promise<VectorData> {
        return new Promise((resolve, reject) => {
            const pythonScriptPath = path.join(
                this._context.extensionPath,
                'python',
                dbType === 'faiss' ? 'faiss_adapter.py' : 'chroma_adapter.py'
            );

            // Check if Python script exists
            if (!fs.existsSync(pythonScriptPath)) {
                reject(new Error(`Python adapter not found: ${pythonScriptPath}`));
                return;
            }

            // Find Python executable
            const pythonCommand = this.getPythonCommand();
            
            // Quote the script path and db path to handle spaces
            const quotedScriptPath = `"${pythonScriptPath}"`;
            const quotedDbPath = `"${dbPath}"`;
            
            // Don't use args array with shell, build the command string instead
            const command = `${pythonCommand} ${quotedScriptPath} ${quotedDbPath}`;
            
            console.log(`[Vector Explorer] Running: ${command}`);
            
            const pythonProcess = spawn(command, [], {
                cwd: this._context.extensionPath,
                shell: true // Use shell to handle path issues on Windows
            });

            let outputData = '';
            let errorData = '';

            pythonProcess.stdout.on('data', (data: Buffer) => {
                outputData += data.toString();
            });

            pythonProcess.stderr.on('data', (data: Buffer) => {
                errorData += data.toString();
                console.error('[Vector Explorer] Python stderr:', data.toString());
            });

            pythonProcess.on('close', (code: number) => {
                if (code !== 0) {
                    reject(new Error(
                        `Python process exited with code ${code}\n` +
                        `Command: ${command}\n` +
                        `Error: ${errorData || 'No error output'}\n` +
                        `Output: ${outputData || 'No output'}`
                    ));
                    return;
                }

                try {
                    const vectorData: VectorData = JSON.parse(outputData);
                    
                    // Check for error in JSON response
                    if ('error' in vectorData) {
                        reject(new Error(`Python adapter error: ${(vectorData as any).error}`));
                        return;
                    }
                    
                    resolve(vectorData);
                } catch (error) {
                    reject(new Error(
                        `Failed to parse Python output: ${error instanceof Error ? error.message : String(error)}\n` +
                        `Output: ${outputData.substring(0, 500)}${outputData.length > 500 ? '...' : ''}`
                    ));
                }
            });

            pythonProcess.on('error', (error: Error) => {
                reject(new Error(
                    `Failed to start Python process: ${error.message}\n` +
                    `Command: ${pythonCommand}\n` +
                    `Make sure Python is installed and in your PATH, or configure vectorExplorer.pythonPath in settings.`
                ));
            });
        });
    }

    private getPythonCommand(): string {
        // Try to get Python command from configuration or environment
        const config = vscode.workspace.getConfiguration('vectorExplorer');
        const customPython = config.get<string>('pythonPath');
        
        if (customPython) {
            return customPython;
        }

        // Default to 'python' - user should have it in PATH
        return process.platform === 'win32' ? 'python' : 'python3';
    }
}
