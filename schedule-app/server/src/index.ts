import express from 'express';
import cors from 'cors';
import dotenv from 'dotenv';
import { schedulesRouter } from './routes/schedules';
import { templatesRouter } from './routes/templates';
import { workersRouter } from './routes/workers';

dotenv.config();

const app = express();
const PORT = process.env.PORT || 3001;

app.use(cors());
app.use(express.json({ limit: '10mb' }));

// API routes
app.use('/api/schedules', schedulesRouter);
app.use('/api/templates', templatesRouter);
app.use('/api/workers', workersRouter);

// Health check
app.get('/api/health', (_req, res) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});

export default app;
