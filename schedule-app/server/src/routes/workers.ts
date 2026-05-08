import { Router, Request, Response } from 'express';
import { prisma } from '../lib/prisma';

export const workersRouter = Router();

// GET all workers
workersRouter.get('/', async (_req: Request, res: Response) => {
  try {
    const workers = await prisma.worker.findMany({
      orderBy: { name: 'asc' },
    });
    res.json(workers);
  } catch (error) {
    console.error('Error fetching workers:', error);
    res.status(500).json({ error: 'Failed to fetch workers' });
  }
});

// POST create worker
workersRouter.post('/', async (req: Request, res: Response) => {
  try {
    const { name, shortName, position } = req.body;
    if (!name || !shortName) {
      res.status(400).json({ error: 'Name and shortName are required' });
      return;
    }
    const worker = await prisma.worker.create({
      data: { name, shortName, position },
    });
    res.status(201).json(worker);
  } catch (error) {
    console.error('Error creating worker:', error);
    res.status(500).json({ error: 'Failed to create worker' });
  }
});

// PUT update worker
workersRouter.put('/:id', async (req: Request, res: Response) => {
  try {
    const id = req.params.id as string;
    const { name, shortName, position } = req.body;
    const worker = await prisma.worker.update({
      where: { id },
      data: {
        ...(name !== undefined && { name }),
        ...(shortName !== undefined && { shortName }),
        ...(position !== undefined && { position }),
      },
    });
    res.json(worker);
  } catch (error) {
    console.error('Error updating worker:', error);
    res.status(500).json({ error: 'Failed to update worker' });
  }
});

// DELETE worker
workersRouter.delete('/:id', async (req: Request, res: Response) => {
  try {
    const id = req.params.id as string;
    await prisma.worker.delete({
      where: { id },
    });
    res.json({ success: true });
  } catch (error) {
    console.error('Error deleting worker:', error);
    res.status(500).json({ error: 'Failed to delete worker' });
  }
});
