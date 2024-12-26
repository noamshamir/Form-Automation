import { useState } from 'react';
import { GeneratedFile } from '../types.ts';

export const useProcessFiles = () => {
    const [isProcessing, setIsProcessing] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [generatedFiles, setGeneratedFiles] = useState<GeneratedFile[]>([]);

    const processFiles = async (
        files: File[],
        plaintiffName: string,
        defendantName: string,
        attorneyName: string
    ) => {
        setIsProcessing(true);
        setError(null);

        try {
            const formData = new FormData();
            files.forEach((file) => {
                formData.append('excel_files', file);
            });
            formData.append('plaintiff_name', plaintiffName);
            formData.append('defendant_name', defendantName);
            formData.append('attorney_name', attorneyName);

            const response = await fetch('http://localhost:3000/api/process-forms', {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new Error(errorData.detail || 'Failed to process files');
            }

            const data = await response.json();
            setGeneratedFiles(data.files.map((file: string) => {
                const filename = file.split('/').pop() || file;
                return {
                    id: Math.random().toString(36).substr(2, 9),
                    name: filename,
                    url: `http://localhost:3000/api/download/${encodeURIComponent(file)}`
                };
            }));
        } catch (err) {
            console.error('Processing error:', err);
            setError(err instanceof Error ? err.message : 'An error occurred while processing files');
        } finally {
            setIsProcessing(false);
        }
    };

    return {
        isProcessing,
        error,
        generatedFiles,
        processFiles,
        setError
    };
};