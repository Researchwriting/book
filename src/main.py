import os
from src.config import Config
from src.generator import get_generator
from src.planner import Planner
from src.writer import Writer
from src.state_manager import StateManager

def main():
    # 1. Setup
    config = Config()
    state_manager = StateManager(config.STATE_FILE)
    state_manager.load()
    
    generator = get_generator(config)
    planner = Planner(generator)
    writer = Writer(generator)
    
    print(f"Starting project: {config.PROJECT_NAME}")
    
    # 2. Idea Generation
    if not state_manager.state.idea:
        print("Generating Idea...")
        idea = planner.generate_idea()
        state_manager.state.idea = idea
        state_manager.save()
        print(f"Idea: {idea}")
    else:
        print(f"Resuming with Idea: {state_manager.state.idea}")

    # 3. Global Outline
    if not state_manager.state.outline:
        print("Creating Global Outline...")
        chapters = planner.create_global_outline(state_manager.state.idea, config.CHAPTERS_COUNT)
        state_manager.state.outline = chapters
        state_manager.save()
        print(f"Created {len(chapters)} chapters.")

    # 4. Generation Loop
    for ch_idx, chapter in enumerate(state_manager.state.outline):
        print(f"Processing {chapter.title}...")
        
        # Ensure scenes exist for this chapter
        if not chapter.scenes:
            print(f"  Creating scenes for {chapter.title}...")
            scenes = planner.create_chapter_outline(chapter, config.SCENES_PER_CHAPTER)
            chapter.scenes = scenes
            state_manager.save()
            
        for sc_idx, scene in enumerate(chapter.scenes):
            if scene.status == "completed":
                continue
                
            print(f"  Writing {scene.title}...")
            
            # Build context (last 500 words of previous scene, or summary)
            context = ""
            if sc_idx > 0:
                context = chapter.scenes[sc_idx-1].content[-500:]
            elif ch_idx > 0:
                # Get last scene of previous chapter
                prev_chapter = state_manager.state.outline[ch_idx-1]
                if prev_chapter.scenes:
                    context = prev_chapter.scenes[-1].content[-500:]
            
            content = writer.write_scene(scene, context)
            state_manager.update_scene_content(ch_idx, sc_idx, content)
            print(f"  Finished {scene.title}. Total Words: {state_manager.state.total_words}")

    print("Generation Complete!")

if __name__ == "__main__":
    main()
