import React, { useEffect } from 'react';
import {
  DndContext,
  closestCenter,
  KeyboardSensor,
  PointerSensor,
  useSensor,
  useSensors,
  type DragEndEvent,
} from '@dnd-kit/core';
import {
  SortableContext,
  sortableKeyboardCoordinates,
  verticalListSortingStrategy,
} from '@dnd-kit/sortable';
import { Plus, Package } from 'lucide-react';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Label } from '@/components/ui/label';
import { ScheduleBlockCard } from './ScheduleBlockCard';
import { useScheduleStore } from '@/store/scheduleStore';
import { DAYS_OF_WEEK } from '@/types/schedule';

export const ScheduleEditor: React.FC = () => {
  const {
    schedule,
    updateDate,
    updateDayOfWeek,
    addBlock,
    addAssemblyBlock,
    reorderBlocks,
  } = useScheduleStore();

  const sensors = useSensors(
    useSensor(PointerSensor, { activationConstraint: { distance: 8 } }),
    useSensor(KeyboardSensor, { coordinateGetter: sortableKeyboardCoordinates })
  );

  const handleDragEnd = (event: DragEndEvent) => {
    const { active, over } = event;
    if (over && active.id !== over.id) {
      const oldIndex = schedule.blocks.findIndex(b => b.id === active.id);
      const newIndex = schedule.blocks.findIndex(b => b.id === over.id);
      reorderBlocks(oldIndex, newIndex);
    }
  };

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.ctrlKey && e.key === 'b') {
        e.preventDefault();
        addBlock();
      }
      if (e.ctrlKey && e.key === 'm') {
        e.preventDefault();
        addAssemblyBlock();
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [addBlock, addAssemblyBlock]);

  return (
    <div className="space-y-4">
      {/* Date & Day Header */}
      <div className="flex items-end gap-4 p-4 rounded-lg bg-muted/50 border">
        <div>
          <Label className="text-xs text-muted-foreground">Дата</Label>
          <Input
            type="date"
            value={schedule.date}
            onChange={e => {
              updateDate(e.target.value);
              const d = new Date(e.target.value + 'T00:00:00');
              const dayIndex = (d.getDay() + 6) % 7;
              updateDayOfWeek(DAYS_OF_WEEK[dayIndex]);
            }}
            className="h-9 w-44"
          />
        </div>
        <div>
          <Label className="text-xs text-muted-foreground">День недели</Label>
          <select
            value={schedule.dayOfWeek}
            onChange={e => updateDayOfWeek(e.target.value)}
            className="flex h-9 w-44 rounded-md border border-input bg-background px-3 py-1 text-sm shadow-sm focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring"
          >
            {DAYS_OF_WEEK.map(day => (
              <option key={day} value={day}>{day}</option>
            ))}
          </select>
        </div>
      </div>

      {/* Blocks */}
      <DndContext sensors={sensors} collisionDetection={closestCenter} onDragEnd={handleDragEnd}>
        <SortableContext items={schedule.blocks.map(b => b.id)} strategy={verticalListSortingStrategy}>
          {schedule.blocks.map(block => (
            <ScheduleBlockCard key={block.id} block={block} />
          ))}
        </SortableContext>
      </DndContext>

      {/* Add Block Buttons */}
      <div className="flex gap-2">
        <Button onClick={addBlock} variant="outline" className="flex-1">
          <Plus className="h-4 w-4 mr-2" />
          Добавить блок
          <span className="ml-2 text-xs text-muted-foreground">(Ctrl+B)</span>
        </Button>
        <Button onClick={addAssemblyBlock} variant="outline" className="flex-1">
          <Package className="h-4 w-4 mr-2" />
          Добавить сборку
          <span className="ml-2 text-xs text-muted-foreground">(Ctrl+M)</span>
        </Button>
      </div>
    </div>
  );
};
