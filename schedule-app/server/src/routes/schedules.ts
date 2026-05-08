import { Router, Request, Response } from 'express';
import { prisma } from '../lib/prisma';
import { generateTelegramText } from '../lib/telegram-generator';

export const schedulesRouter = Router();

// GET all schedules
schedulesRouter.get('/', async (_req: Request, res: Response) => {
  try {
    const schedules = await prisma.schedule.findMany({
      orderBy: { updatedAt: 'desc' },
    });
    res.json(schedules);
  } catch (error) {
    console.error('Error fetching schedules:', error);
    res.status(500).json({ error: 'Failed to fetch schedules' });
  }
});

// GET single schedule
schedulesRouter.get('/:id', async (req: Request, res: Response) => {
  try {
    const id = req.params.id as string;
    const schedule = await prisma.schedule.findUnique({
      where: { id },
    });
    if (!schedule) {
      res.status(404).json({ error: 'Schedule not found' });
      return;
    }
    res.json(schedule);
  } catch (error) {
    console.error('Error fetching schedule:', error);
    res.status(500).json({ error: 'Failed to fetch schedule' });
  }
});

// POST create schedule
schedulesRouter.post('/', async (req: Request, res: Response) => {
  try {
    const { date, dayOfWeek, blocks, isDraft } = req.body;
    if (!date || !dayOfWeek) {
      res.status(400).json({ error: 'Date and dayOfWeek are required' });
      return;
    }
    const schedule = await prisma.schedule.create({
      data: {
        date,
        dayOfWeek,
        blocks: blocks || [],
        isDraft: isDraft ?? true,
      },
    });
    res.status(201).json(schedule);
  } catch (error) {
    console.error('Error creating schedule:', error);
    res.status(500).json({ error: 'Failed to create schedule' });
  }
});

// PUT update schedule
schedulesRouter.put('/:id', async (req: Request, res: Response) => {
  try {
    const id = req.params.id as string;
    const { date, dayOfWeek, blocks, isDraft } = req.body;
    const schedule = await prisma.schedule.update({
      where: { id },
      data: {
        ...(date !== undefined && { date }),
        ...(dayOfWeek !== undefined && { dayOfWeek }),
        ...(blocks !== undefined && { blocks }),
        ...(isDraft !== undefined && { isDraft }),
      },
    });
    res.json(schedule);
  } catch (error) {
    console.error('Error updating schedule:', error);
    res.status(500).json({ error: 'Failed to update schedule' });
  }
});

// PUT autosave
schedulesRouter.put('/:id/autosave', async (req: Request, res: Response) => {
  try {
    const id = req.params.id as string;
    const { date, dayOfWeek, blocks } = req.body;
    const schedule = await prisma.schedule.update({
      where: { id },
      data: {
        ...(date !== undefined && { date }),
        ...(dayOfWeek !== undefined && { dayOfWeek }),
        ...(blocks !== undefined && { blocks }),
      },
    });
    res.json(schedule);
  } catch (error) {
    console.error('Error autosaving:', error);
    res.status(500).json({ error: 'Failed to autosave' });
  }
});

// DELETE schedule
schedulesRouter.delete('/:id', async (req: Request, res: Response) => {
  try {
    const id = req.params.id as string;
    await prisma.schedule.delete({
      where: { id },
    });
    res.json({ success: true });
  } catch (error) {
    console.error('Error deleting schedule:', error);
    res.status(500).json({ error: 'Failed to delete schedule' });
  }
});

// GET generate telegram text
schedulesRouter.get('/:id/generate', async (req: Request, res: Response) => {
  try {
    const id = req.params.id as string;
    const schedule = await prisma.schedule.findUnique({
      where: { id },
    });
    if (!schedule) {
      res.status(404).json({ error: 'Schedule not found' });
      return;
    }
    const text = generateTelegramText(schedule);
    res.json({ text });
  } catch (error) {
    console.error('Error generating text:', error);
    res.status(500).json({ error: 'Failed to generate text' });
  }
});
