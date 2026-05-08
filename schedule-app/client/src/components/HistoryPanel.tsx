import React, { useEffect } from 'react';
import { Trash2, FileText, Calendar } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { useScheduleStore } from '@/store/scheduleStore';

export const HistoryPanel: React.FC = () => {
  const { schedules, loadSchedules, loadSchedule, deleteSchedule } = useScheduleStore();

  useEffect(() => {
    loadSchedules();
  }, [loadSchedules]);

  if (schedules.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center py-16 text-muted-foreground">
        <FileText className="h-12 w-12 mb-4 opacity-50" />
        <p className="text-lg font-medium">Нет сохранённых расписаний</p>
        <p className="text-sm">Создайте и сохраните расписание, чтобы оно появилось здесь</p>
      </div>
    );
  }

  return (
    <div className="space-y-3">
      <h3 className="font-semibold text-lg">История расписаний</h3>
      {schedules.map(s => (
        <Card key={s.id} className="hover:border-primary/50 transition-colors cursor-pointer" onClick={() => loadSchedule(s.id)}>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <Calendar className="h-5 w-5 text-muted-foreground" />
                <div>
                  <p className="font-medium">{s.date} {s.dayOfWeek}</p>
                  <p className="text-xs text-muted-foreground">
                    {s.blocks.length} блоков &middot; {new Date(s.updatedAt).toLocaleString('ru-RU')}
                  </p>
                </div>
              </div>
              <Button
                variant="ghost"
                size="icon"
                className="h-8 w-8 text-destructive"
                onClick={e => { e.stopPropagation(); deleteSchedule(s.id); }}
              >
                <Trash2 className="h-4 w-4" />
              </Button>
            </div>
          </CardContent>
        </Card>
      ))}
    </div>
  );
};
