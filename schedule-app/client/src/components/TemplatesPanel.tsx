import React, { useEffect, useState } from 'react';
import { Trash2, LayoutTemplate, Save } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent } from '@/components/ui/card';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
  DialogClose,
} from '@/components/ui/dialog';
import { useScheduleStore } from '@/store/scheduleStore';

export const TemplatesPanel: React.FC = () => {
  const { templates, loadTemplates, saveAsTemplate, loadTemplate, deleteTemplate } = useScheduleStore();
  const [templateName, setTemplateName] = useState('');
  const [dialogOpen, setDialogOpen] = useState(false);

  useEffect(() => {
    loadTemplates();
  }, [loadTemplates]);

  const handleSave = async () => {
    if (!templateName.trim()) return;
    await saveAsTemplate(templateName.trim());
    setTemplateName('');
    setDialogOpen(false);
  };

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h3 className="font-semibold text-lg">Шаблоны</h3>
        <Dialog open={dialogOpen} onOpenChange={setDialogOpen}>
          <DialogTrigger asChild>
            <Button variant="outline" size="sm">
              <Save className="h-4 w-4 mr-1" />
              Сохранить как шаблон
            </Button>
          </DialogTrigger>
          <DialogContent>
            <DialogHeader>
              <DialogTitle>Сохранить шаблон</DialogTitle>
            </DialogHeader>
            <div className="space-y-4">
              <Input
                placeholder="Название шаблона"
                value={templateName}
                onChange={e => setTemplateName(e.target.value)}
                onKeyDown={e => { if (e.key === 'Enter') handleSave(); }}
                autoFocus
              />
              <div className="flex gap-2 justify-end">
                <DialogClose asChild>
                  <Button variant="outline">Отмена</Button>
                </DialogClose>
                <Button onClick={handleSave} disabled={!templateName.trim()}>
                  Сохранить
                </Button>
              </div>
            </div>
          </DialogContent>
        </Dialog>
      </div>

      {templates.length === 0 ? (
        <div className="flex flex-col items-center justify-center py-16 text-muted-foreground">
          <LayoutTemplate className="h-12 w-12 mb-4 opacity-50" />
          <p className="text-lg font-medium">Нет шаблонов</p>
          <p className="text-sm">Сохраните текущее расписание как шаблон</p>
        </div>
      ) : (
        <div className="space-y-3">
          {templates.map(t => (
            <Card key={t.id} className="hover:border-primary/50 transition-colors cursor-pointer" onClick={() => loadTemplate(t)}>
              <CardContent className="p-4">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <LayoutTemplate className="h-5 w-5 text-muted-foreground" />
                    <div>
                      <p className="font-medium">{t.name}</p>
                      <p className="text-xs text-muted-foreground">
                        {t.blocks.length} блоков &middot; {new Date(t.createdAt).toLocaleString('ru-RU')}
                      </p>
                    </div>
                  </div>
                  <Button
                    variant="ghost"
                    size="icon"
                    className="h-8 w-8 text-destructive"
                    onClick={e => { e.stopPropagation(); deleteTemplate(t.id); }}
                  >
                    <Trash2 className="h-4 w-4" />
                  </Button>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
};
