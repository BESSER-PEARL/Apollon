import React from 'react';
import MonacoEditor from '@monaco-editor/react';

interface CodeBlockProps {
  code: string;
  language?: string;
  onChange: (value: string) => void;
}

export const CodeBlock: React.FC<CodeBlockProps> = ({
  code,
  language = 'javascript', 
  onChange
}) => {
  return (
    <div style={{ height: 200, border: '1px solid #ccc' }}>
      <MonacoEditor
        value={code}
        language={language}
        onChange={(value) => onChange(value || '')}
        options={{
          minimap: { enabled: false },
          scrollBeyondLastLine: false,
          fontSize: 14,
          lineNumbers: 'on',
          automaticLayout: true,
          wordWrap: 'on'
        }}
      />
    </div>
  );
};
