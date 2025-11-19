#!/usr/bin/env python3
"""
System Integration Test - Verify all components work together
"""
import os
import sys

def test_system_integration():
    print("=" * 70)
    print("🧪 SYSTEM INTEGRATION TEST")
    print("=" * 70)
    print("\nTesting all components...\n")
    
    results = {}
    
    # Test 1: Config
    print("[1/10] Testing configuration...")
    try:
        from src.config import Config
        config = Config()
        assert config.PROVIDER is not None
        assert config.API_KEY is not None
        results['config'] = '✅ PASS'
    except Exception as e:
        results['config'] = f'❌ FAIL: {e}'
    
    # Test 2: Generator
    print("[2/10] Testing LLM generator...")
    try:
        from src.generator import get_generator
        generator = get_generator(config)
        assert generator is not None
        results['generator'] = '✅ PASS'
    except Exception as e:
        results['generator'] = f'❌ FAIL: {e}'
    
    # Test 3: Syllabus Parser
    print("[3/10] Testing syllabus parser...")
    try:
        from src.syllabus_parser import parse_syllabus
        # Create test file
        with open('test_syllabus.md', 'w') as f:
            f.write("# Test\n## 1. Section One\n## 2. Section Two\n")
        sections = parse_syllabus('test_syllabus.md')
        assert len(sections) == 2
        os.remove('test_syllabus.md')
        results['parser'] = '✅ PASS'
    except Exception as e:
        results['parser'] = f'❌ FAIL: {e}'
    
    # Test 4: Master Command Generator
    print("[4/10] Testing master command generator...")
    try:
        from src.master_command_generator import generate_master_command
        test_section = {
            'chapter': 'Test Chapter',
            'section_number': '1',
            'section_title': 'Test Section'
        }
        mc = generate_master_command(test_section)
        assert len(mc) > 0
        results['master_command'] = '✅ PASS'
    except Exception as e:
        results['master_command'] = f'❌ FAIL: {e}'
    
    # Test 5: Quality Control
    print("[5/10] Testing quality control...")
    try:
        from src.quality_control import check_quality
        test_content = "This is a test paragraph with proper prose.\n\nFigure 1.1: Test\n\nTable 1.1: Test"
        report = check_quality(test_content, "Test")
        assert report is not None
        results['quality_control'] = '✅ PASS'
    except Exception as e:
        results['quality_control'] = f'❌ FAIL: {e}'
    
    # Test 6: Cost Tracker
    print("[6/10] Testing cost tracker...")
    try:
        from src.cost_tracker import cost_tracker
        cost_tracker.estimate_tokens("test prompt", is_input=True)
        summary = cost_tracker.get_summary()
        assert 'total_tokens' in summary
        results['cost_tracker'] = '✅ PASS'
    except Exception as e:
        results['cost_tracker'] = f'❌ FAIL: {e}'
    
    # Test 7: Resume Manager
    print("[7/10] Testing resume manager...")
    try:
        from src.resume_manager import resume_manager
        resume_manager.start_section("test", "Test Section", 5)
        resume_manager.complete_subsection("test", 1, 1)
        assert resume_manager.is_subsection_completed("test", 1, 1)
        resume_manager.clear_section("test")
        results['resume_manager'] = '✅ PASS'
    except Exception as e:
        results['resume_manager'] = f'❌ FAIL: {e}'
    
    # Test 8: Parallel Generator
    print("[8/10] Testing parallel generator...")
    try:
        from src.parallel_generator import ParallelGenerator
        pg = ParallelGenerator(max_workers=2)
        assert pg.max_workers == 2
        results['parallel_generator'] = '✅ PASS'
    except Exception as e:
        results['parallel_generator'] = f'❌ FAIL: {e}'
    
    # Test 9: Model Switcher
    print("[9/10] Testing model switcher...")
    try:
        from src.model_switcher import get_current_model, compare_costs
        model_name = get_current_model(config)
        assert model_name is not None
        results['model_switcher'] = '✅ PASS'
    except Exception as e:
        results['model_switcher'] = f'❌ FAIL: {e}'
    
    # Test 10: Auto Notifier
    print("[10/10] Testing auto notifier...")
    try:
        from src.auto_notifier import load_notification_config
        notif_config = load_notification_config()
        # Just check it doesn't crash
        results['auto_notifier'] = '✅ PASS'
    except Exception as e:
        results['auto_notifier'] = f'❌ FAIL: {e}'
    
    # Print results
    print("\n" + "=" * 70)
    print("TEST RESULTS")
    print("=" * 70 + "\n")
    
    passed = 0
    failed = 0
    
    for component, result in results.items():
        print(f"{component:20s} {result}")
        if '✅' in result:
            passed += 1
        else:
            failed += 1
    
    print("\n" + "=" * 70)
    print(f"SUMMARY: {passed} passed, {failed} failed")
    print("=" * 70)
    
    if failed == 0:
        print("\n🎉 ALL TESTS PASSED! System is fully integrated and working!")
        print("\nYou can now:")
        print("  1. Run: python3 generate.py")
        print("  2. Run: python3 -m src.interactive_main")
        print("  3. Run: python3 -m src.batch_processor")
    else:
        print("\n⚠️  Some tests failed. Please check the errors above.")
    
    return failed == 0

if __name__ == "__main__":
    success = test_system_integration()
    sys.exit(0 if success else 1)
