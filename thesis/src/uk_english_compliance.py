"""
UK English and Grammar Compliance Module
Ensures all generated content uses UK English spelling and appropriate tenses
"""

class UKEnglishCompliance:
    """Enforce UK English spelling and grammar"""
    
    # US to UK spelling mappings
    US_TO_UK = {
        'analyze': 'analyse',
        'analyzed': 'analysed',
        'analyzing': 'analysing',
        'analyzer': 'analyser',
        'organization': 'organisation',
        'organizations': 'organisations',
        'organizational': 'organisational',
        'labor': 'labour',
        'labored': 'laboured',
        'behavior': 'behaviour',
        'behavioral': 'behavioural',
        'center': 'centre',
        'centered': 'centred',
        'program': 'programme',  # Except computer programs
        'programs': 'programmes',
        'defense': 'defence',
        'offense': 'offence',
        'license': 'licence',  # Noun form
        'practice': 'practise',  # Verb form
        'realize': 'realise',
        'realized': 'realised',
        'realizing': 'realising',
        'recognize': 'recognise',
        'recognized': 'recognised',
        'recognizing': 'recognising',
        'utilize': 'utilise',
        'utilized': 'utilised',
        'utilizing': 'utilising',
        'color': 'colour',
        'colored': 'coloured',
        'favor': 'favour',
        'favored': 'favoured',
        'honor': 'honour',
        'honored': 'honoured',
        'neighbor': 'neighbour',
        'neighbors': 'neighbours',
        'flavor': 'flavour',
        'flavored': 'flavoured',
        'harbor': 'harbour',
        'harbored': 'harboured',
        'humor': 'humour',
        'humored': 'humoured',
        'rumor': 'rumour',
        'rumors': 'rumours',
        'tumor': 'tumour',
        'tumors': 'tumours',
        'vapor': 'vapour',
        'vapors': 'vapours',
        'vigor': 'vigour',
        'vigorous': 'vigorous',  # No change
        'endeavor': 'endeavour',
        'endeavored': 'endeavoured',
        'fulfill': 'fulfil',
        'fulfilled': 'fulfilled',  # Double L kept
        'fulfilling': 'fulfilling',
        'skillful': 'skilful',
        'willful': 'wilful',
        'traveled': 'travelled',
        'traveling': 'travelling',
        'traveler': 'traveller',
        'canceled': 'cancelled',
        'canceling': 'cancelling',
        'labeled': 'labelled',
        'labeling': 'labelling',
        'modeled': 'modelled',
        'modeling': 'modelling',
        'counselor': 'counsellor',
        'counseled': 'counselled',
        'counseling': 'counselling',
        'jewelry': 'jewellery',
        'check': 'cheque',  # For bank cheques only
        'gray': 'grey',
        'aging': 'ageing',
        'dialog': 'dialogue',
        'catalog': 'catalogue',
        'analog': 'analogue',
        'skeptic': 'sceptic',
        'skeptical': 'sceptical',
        'skepticism': 'scepticism',
        'esthetic': 'aesthetic',
        'esthetics': 'aesthetics',
        'maneuver': 'manoeuvre',
        'maneuvered': 'manoeuvred',
        'maneuvering': 'manoeuvring',
        'pediatric': 'paediatric',
        'pediatrics': 'paediatrics',
        'encyclopedia': 'encyclopaedia',
        'medieval': 'mediaeval',
        'archeology': 'archaeology',
        'archeological': 'archaeological',
    }
    
    @classmethod
    def convert_to_uk(cls, text):
        """Convert US English to UK English"""
        for us_word, uk_word in cls.US_TO_UK.items():
            # Case-insensitive replacement
            import re
            pattern = re.compile(re.escape(us_word), re.IGNORECASE)
            
            def replace_match(match):
                matched_text = match.group(0)
                if matched_text.isupper():
                    return uk_word.upper()
                elif matched_text[0].isupper():
                    return uk_word.capitalize()
                else:
                    return uk_word
            
            text = pattern.sub(replace_match, text)
        
        return text
    
    @classmethod
    def get_chapter_tense_guidelines(cls, chapter_num):
        """Get tense guidelines for each chapter"""
        guidelines = {
            1: {
                'background': 'past',
                'problem_statement': 'present',
                'objectives': 'infinitive',  # "To examine...", "To determine..."
                'significance': 'future/present',
                'scope': 'present'
            },
            2: {
                'past_studies': 'past',
                'current_gaps': 'present',
                'synthesis': 'past',
                'theories': 'past/present'
            },
            3: {
                'research_design': 'past',
                'procedures': 'past',
                'instruments': 'past',
                'sampling': 'past',
                'data_collection': 'past'
            },
            4: {
                'results': 'past',
                'presentation': 'past',
                'interpretation': 'past',
                'no_discussion': True
            },
            5: {
                'discussion': 'present/past',
                'implications': 'present',
                'comparison': 'past'
            },
            6: {
                'summary': 'past',
                'conclusions': 'present',
                'recommendations': 'present/future'
            }
        }
        
        return guidelines.get(chapter_num, {})
    
    @classmethod
    def get_system_prompt_suffix(cls, chapter_num):
        """Get UK English and tense instructions for system prompts"""
        tense_guide = cls.get_chapter_tense_guidelines(chapter_num)
        
        suffix = "\n\nIMPORTANT LANGUAGE REQUIREMENTS:\n"
        suffix += "1. Use UK English spelling throughout (analyse, organisation, behaviour, centre, etc.)\n"
        suffix += "2. Use 'data were' (not 'data was') - data is plural in UK English\n"
        suffix += "3. Use appropriate tenses:\n"
        
        if chapter_num == 1:
            suffix += "   - Background: past tense ('The conflict began...', 'Studies showed...')\n"
            suffix += "   - Problem statement: present tense ('The problem is...', 'There exists...')\n"
            suffix += "   - Objectives: infinitive ('To examine...', 'To determine...')\n"
            suffix += "   - Significance: present/future ('This study will contribute...')\n"
        
        elif chapter_num == 2:
            suffix += "   - Past studies: past tense ('Smith (2020) found...', 'The study revealed...')\n"
            suffix += "   - Current gaps: present tense ('There is limited research...', 'Few studies exist...')\n"
            suffix += "   - Synthesis: past tense ('Research demonstrated...', 'Evidence showed...')\n"
        
        elif chapter_num == 3:
            suffix += "   - All methodology: past tense ('The study employed...', 'Data were collected...')\n"
            suffix += "   - Procedures: past tense ('Questionnaires were distributed...', 'Participants were selected...')\n"
        
        elif chapter_num == 4:
            suffix += "   - All results: past tense ('The data showed...', 'Respondents indicated...', 'The mean was...')\n"
            suffix += "   - Presentation: past tense ('Table 4.1 presented...', 'The distribution revealed...')\n"
            suffix += "   - NO DISCUSSION - only present and interpret results\n"
        
        suffix += "4. Use flowing academic prose - avoid bulleting except for objectives/questions lists\n"
        suffix += "5. Maintain formal academic tone throughout\n"
        
        return suffix


class GrammarChecker:
    """Check for common grammar issues"""
    
    @classmethod
    def check_common_errors(cls, text):
        """Check for common grammar errors"""
        errors = []
        
        # Check for "data was" (should be "data were")
        if 'data was' in text.lower():
            errors.append("Use 'data were' instead of 'data was' (UK English)")
        
        # Check for "different than" (should be "different from")
        if 'different than' in text.lower():
            errors.append("Use 'different from' instead of 'different than' (UK English)")
        
        # Check for US spellings
        us_words_found = []
        for us_word in UKEnglishCompliance.US_TO_UK.keys():
            if us_word in text.lower():
                us_words_found.append(f"{us_word} → {UKEnglishCompliance.US_TO_UK[us_word]}")
        
        if us_words_found:
            errors.append(f"US spellings found: {', '.join(us_words_found[:5])}")
        
        return errors
