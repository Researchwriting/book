"""
Parallel Generator - Generate multiple sections simultaneously
"""
import threading
import queue
import time
from typing import List, Dict, Callable

class ParallelGenerator:
    def __init__(self, max_workers: int = 2):
        """
        Initialize parallel generator.
        
        Args:
            max_workers: Maximum number of sections to generate simultaneously
        """
        self.max_workers = max_workers
        self.task_queue = queue.Queue()
        self.results = {}
        self.errors = {}
        self.lock = threading.Lock()
        self.active_workers = 0
    
    def worker(self, worker_id: int, generate_func: Callable):
        """
        Worker thread that processes tasks from the queue.
        
        Args:
            worker_id: Unique ID for this worker
            generate_func: Function to call for generation
        """
        while True:
            try:
                # Get task from queue (with timeout to allow checking for completion)
                task = self.task_queue.get(timeout=1)
                
                if task is None:  # Poison pill to stop worker
                    break
                
                section_info, section_idx, total_sections = task
                section_num = section_info['section_number']
                
                print(f"\n🔄 [Worker {worker_id}] Starting Section {section_num}")
                
                try:
                    # Call the generation function
                    generate_func(section_info, section_idx, total_sections)
                    
                    with self.lock:
                        self.results[section_num] = 'success'
                    
                    print(f"\n✅ [Worker {worker_id}] Completed Section {section_num}")
                
                except Exception as e:
                    with self.lock:
                        self.errors[section_num] = str(e)
                    print(f"\n❌ [Worker {worker_id}] Error in Section {section_num}: {e}")
                
                finally:
                    self.task_queue.task_done()
            
            except queue.Empty:
                # No tasks available, check if we should continue
                with self.lock:
                    if self.task_queue.empty() and self.active_workers == 0:
                        break
    
    def generate_parallel(self, sections: List[Dict], generate_func: Callable):
        """
        Generate multiple sections in parallel.
        
        Args:
            sections: List of section info dicts
            generate_func: Function to call for each section
        """
        total_sections = len(sections)
        
        # Add all tasks to queue
        for idx, section_info in enumerate(sections, 1):
            self.task_queue.put((section_info, idx, total_sections))
        
        # Create worker threads
        workers = []
        for i in range(min(self.max_workers, len(sections))):
            worker = threading.Thread(
                target=self.worker,
                args=(i + 1, generate_func),
                daemon=True
            )
            worker.start()
            workers.append(worker)
            
            with self.lock:
                self.active_workers += 1
        
        # Wait for all tasks to complete
        self.task_queue.join()
        
        # Stop workers
        for _ in workers:
            self.task_queue.put(None)
        
        # Wait for workers to finish
        for worker in workers:
            worker.join()
        
        return self.results, self.errors
    
    def get_status(self) -> Dict:
        """Get current status of parallel generation."""
        with self.lock:
            return {
                'completed': len(self.results),
                'errors': len(self.errors),
                'pending': self.task_queue.qsize(),
                'active_workers': self.active_workers
            }

# Global instance
parallel_generator = ParallelGenerator(max_workers=2)
