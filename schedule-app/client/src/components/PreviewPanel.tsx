import React, { useState } from 'react';
import { Copy, Download, Check, RefreshCw } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { useScheduleStore } from '@/store/scheduleStore';

export const PreviewPanel: React.FC = () => {
  const { generatedText, generateText, copyText, exportTxt } = useScheduleStore();
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    const ok = await copyText();
    if (ok) {
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h3 className="font-semibold text-lg">Предпросмотр</h3>
        <div className="flex gap-2">
          <Button onClick={generateText} variant="default" size="sm">
            <RefreshCw className="h-4 w-4 mr-1" />
            Сгенерировать
          </Button>
          <Button onClick={handleCopy} variant="outline" size="sm" disabled={!generatedText}>
            {copied ? <Check className="h-4 w-4 mr-1 text-green-600" /> : <Copy className="h-4 w-4 mr-1" />}
            {copied ? 'Скопировано!' : 'Копировать'}
          </Button>
          <Button onClick={exportTxt} variant="outline" size="sm" disabled={!generatedText}>
            <Download className="h-4 w-4 mr-1" />
            TXT
          </Button>
        </div>
      </div>

      <div className="min-h-96 rounded-lg border bg-white p-4 font-mono text-sm whitespace-pre-wrap leading-relaxed">
        {generatedText || (
          <span className="text-muted-foreground italic">
            Нажмите «Сгенерировать расписание» для предпросмотра
          </span>
        )}
      </div>
    </div>
  );
};
