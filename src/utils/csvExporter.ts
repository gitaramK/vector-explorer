import * as vscode from 'vscode';
import * as path from 'path';
import * as fs from 'fs';
import { stringify } from 'csv-stringify/sync';
import { VectorData } from '../types';

export async function exportToCSV(data: VectorData): Promise<void> {
    const saveUri = await vscode.window.showSaveDialog({
        defaultUri: vscode.Uri.file('vector_export.csv'),
        filters: {
            'CSV Files': ['csv'],
            'All Files': ['*']
        }
    });

    if (!saveUri) {
        return;
    }

    try {
        // Prepare CSV data
        const csvData = data.vectors.map(vector => ({
            id: vector.id,
            text: vector.text,
            source: vector.source,
            vector: JSON.stringify(vector.vector),
            dimension: vector.vector.length,
            metadata: JSON.stringify(vector.metadata || {})
        }));

        const csv = stringify(csvData, {
            header: true,
            columns: ['id', 'text', 'source', 'vector', 'dimension', 'metadata']
        });

        // Write to file
        fs.writeFileSync(saveUri.fsPath, csv, 'utf-8');
    } catch (error) {
        throw new Error(`Failed to export CSV: ${error instanceof Error ? error.message : String(error)}`);
    }
}
