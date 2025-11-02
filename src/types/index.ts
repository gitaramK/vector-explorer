export interface VectorData {
    type: 'faiss' | 'chroma';
    count: number;
    dimension: number;
    vectors: VectorRecord[];
}

export interface VectorRecord {
    id: string;
    vector: number[];
    text: string;
    source: string;
    metadata?: Record<string, any>;
}

export interface WebviewMessage {
    type: string;
    [key: string]: any;
}

export interface FAISSMetadata {
    chunks: Array<{
        id: string;
        text: string;
        source: string;
        metadata?: Record<string, any>;
    }>;
}
