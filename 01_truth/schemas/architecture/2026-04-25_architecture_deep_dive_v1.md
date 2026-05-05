---
title: "SWARMS ARCHITECTURE DEEP DIVE & ADAPTATION GUIDE"
id: "architecture_deep_dive"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "architecture"
audience: "internal"
layer: "truth"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# SWARMS ARCHITECTURE DEEP DIVE & ADAPTATION GUIDE

## 🎓 UNDERSTANDING THE SWARMS FRAMEWORK

### What is Swarms?

Swarms is a **multi-agent orchestration framework** that enables:
- Multiple AI agents working together
- Specialized roles for each agent
- Coordinated workflows
- State management across agents
- Error recovery and retry logic

**Think of it as**: A conductor (orchestrator) leading an orchestra (specialized agents)

---

## 🏗️ PRODUCT MARKETING AGENCY ARCHITECTURE

### The 6 Agents Explained

#### 1. Orchestrator Agent
```python
self.orchestrator_agent = Agent(
    agent_name="Marketing-Orchestrator",
    agent_description="Central coordinator for marketing campaigns",
    model_name="gemini-2.0-flash-exp",
    max_loops=1,
    dynamic_temperature_enabled=True,
    dynamic_context_window=True,
    retry_interval=2,
)
```

**Role**: Project manager
**Responsibilities**:
- Validates input
- Coordinates other agents
- Handles errors
- Reports progress

**Swarms Pattern**: **Coordinator Pattern**
- One agent manages others
- No direct work execution
- Focuses on flow control

**When to call**:
```python
# Not called directly - works behind the scenes
# Orchestrator is implicit in run_marketing_campaign()
```

---

#### 2. Product Interpreter Agent
```python
self.product_interpreter_agent = Agent(
    agent_name="Product-Interpreter",
    agent_description="Analyzes product information",
    model_name="gemini-2.0-flash-exp",
    max_loops=1,
    ...
)
```

**Role**: Data analyst
**Responsibilities**:
- Parses product descriptions
- Extracts structured data
- Creates ProductProfile objects
- Validates completeness

**Swarms Pattern**: **Transformer Pattern**
- Takes unstructured input
- Returns structured output

**Example Call**:
```python
product_profile = self.product_interpreter_agent.run(
    f"Analyze this product: {raw_description}"
)
```

**Key Insight**: Uses dynamic temperature (creative when needed, consistent when parsing)

---

#### 3. Image Type Selector Agent
```python
self.image_selector_agent = Agent(
    agent_name="Image-Type-Selector",
    agent_description="Returns ONLY numbers for image type selection",
    model_name="gemini-2.0-flash-exp",
    max_loops=1,
    ...
)
```

**Role**: Strategic advisor
**Responsibilities**:
- Analyzes product category
- Selects appropriate image types
- Returns numbers (1-10)
- Considers target audience

**Swarms Pattern**: **Decision Maker Pattern**
- Limited output format
- Clear choices
- No ambiguity

**Example Prompt**:
```python
prompt = f"""
Given this product:
- Category: {category}
- Target: {audience}

Select 3-5 image types (numbers only):
1. Master Shot
2. Flat Lay
...
10. Shop the Look

Return ONLY comma-separated numbers.
"""
```

**Why This Works**:
- Constrained output = reliable parsing
- Numbers are easy to validate
- Prevents hallucination

---

#### 4. Prompt Generator Agent
```python
self.prompt_generator_agent = Agent(
    agent_name="Prompt-Generator",
    agent_description="Generates customized prompts",
    model_name="gemini-2.0-flash-exp",
    max_loops=1,
    ...
)
```

**Role**: Creative director
**Responsibilities**:
- Creates detailed image prompts
- Incorporates brand guidelines
- Tailors to image type
- Optimizes for generation quality

**Swarms Pattern**: **Template Expansion Pattern**
- Takes structured data
- Creates rich, detailed prompts
- Maintains consistency

**Example Template**:
```python
template = f"""
Create a {image_type} image of {product_name}.

Key features:
{features}

Brand colors: {colors}
Target audience: {audience}

Style requirements:
- Professional product photography
- Studio lighting
- {image_type_specific_details}

Composition:
{composition_guidelines}
"""
```

**Pro Tip**: This is where quality is made or broken. Invest time here!

---

#### 5. Image Generation Agent ("Banana-Nano")
```python
self.image_generation_agent = Agent(
    agent_name="Banana-Nano-Generator",
    agent_description="Creates high-quality marketing images",
    model_name="gemini-2.5-flash-image-preview",  # MULTIMODAL
    max_loops=1,
    system_prompt="Generate images immediately. No explanations.",
    ...
)
```

**Role**: Artist/executor
**Responsibilities**:
- Generates actual images
- Returns base64 or URLs
- Maintains quality
- Handles generation errors

**Swarms Pattern**: **Generator Pattern**
- Takes prompt → produces artifact
- Different model type (multimodal)
- Fresh instance per image

**Why Fresh Agents?**:
```python
def _create_fresh_image_agent(self) -> Agent:
    """
    Create a NEW agent for each image to prevent:
    - Context contamination
    - Style drift
    - Memory leaks
    """
    return Agent(...)
```

**Critical**: Prevents one image's style from influencing the next

---

#### 6. Output Handler Agent
```python
self.output_handler_agent = Agent(
    agent_name="Output-Handler-Feedback",
    agent_description="Manages output and feedback",
    model_name="gemini-2.0-flash-exp",
    max_loops=1,
    ...
)
```

**Role**: Quality assurance & reporter
**Responsibilities**:
- Validates generated images
- Saves to correct locations
- Generates reports
- Processes feedback

**Swarms Pattern**: **Finalizer Pattern**
- Last step in pipeline
- Cleanup and delivery
- Feedback loop

---

## 🔄 DATA FLOW ANALYSIS

### Complete Workflow with Data Types

```
USER INPUT (String)
↓
"Smart Water Bottle with temp control, $50, eco-friendly"

├─→ Product Interpreter Agent
│   Input:  String (raw description)
│   Output: ProductProfile (structured data)
│   {
│     product_name: "Smart Water Bottle",
│     category: "Home & Kitchen",
│     features: ["temp control", "eco-friendly"],
│     price_range: "$50",
│     ...
│   }
│
├─→ Image Type Selector Agent
│   Input:  ProductProfile
│   Output: List[int] (image type numbers)
│   [1, 7, 9]  # Master, Lifestyle, Banner
│
└─→ FOR EACH image type:
    │
    ├─→ Prompt Generator Agent
    │   Input:  ProductProfile + ImageType
    │   Output: String (detailed prompt)
    │   "Professional studio shot of Smart Water Bottle,
    │    featuring temperature control display, eco-friendly
    │    materials visible, soft lighting..."
    │
    ├─→ Image Generation Agent (Fresh!)
    │   Input:  String (prompt)
    │   Output: bytes (base64 image) or URL
    │   <image_data>
    │
    └─→ Output Handler Agent
        Input:  Image data + metadata
        Output: File path + report
        "./marketing_outputs/products/SmartBottle/master_shot.png"
```

### Type Safety with Dataclasses

```python
@dataclass
class ProductProfile:
    """Ensures type safety across agents"""
    product_name: str
    category: str
    key_features: List[str]
    accessories: List[str]
    objectives: List[str]
    suggested_image_types: List[int]
    product_id: str = None
    master_image_path: Optional[str] = None
    timestamp: str = None

@dataclass
class MarketingJob:
    """Tracks individual generation tasks"""
    job_id: str
    product_profile: ProductProfile
    image_type: ImageType
    custom_requirements: str = ""
    output_path: Optional[str] = None
    status: str = "pending"
    created_at: str = None
```

**Benefits**:
- Type hints for IDE support
- Validation at runtime
- Clear contracts between agents
- Easy serialization (asdict())

---

## 🎯 SWARMS PATTERNS DEMONSTRATED

### 1. Pipeline Pattern
**Sequential agent execution**

```python
# Product → Interpreter → Selector → Generator
result = (
    orchestrator
    .then(interpreter)
    .then(selector)
    .then(generator)
    .execute(input_data)
)
```

**When to use**: Linear workflows

---

### 2. Fan-Out Pattern
**One task spawns multiple parallel tasks**

```python
# One product → Multiple image types in parallel
for image_type in selected_types:
    jobs.append(generate_image_async(profile, image_type))

results = await gather(*jobs)
```

**When to use**: Independent parallel tasks

---

### 3. Map-Reduce Pattern
**Process items individually, aggregate results**

```python
# Batch processing
def map_function(product):
    return generate_campaign(product)

def reduce_function(results):
    return aggregate_statistics(results)

# Map
individual_results = [map_function(p) for p in products]
# Reduce
summary = reduce_function(individual_results)
```

**When to use**: Batch operations with aggregation

---

### 4. Retry Pattern
**Automatic error recovery**

```python
self.image_generation_agent = Agent(
    retry_interval=2,          # Wait 2s between retries
    dynamic_temperature_enabled=True,  # Adjust creativity on retry
)
```

**Built into Swarms**: No manual try-catch needed

---

### 5. Circuit Breaker Pattern
**Stop calling failing services**

```python
if consecutive_failures > MAX_FAILURES:
    switch_to_fallback_model()
    # or
    notify_admin()
    # or
    graceful_degradation()
```

**Implementation**: Custom in orchestrator

---

## 🔧 ADAPTING FOR SERVICE BUSINESSES

### Your Use Case: Dental/Vet/Salon Marketing

**Current Problem**: Built for physical products
**Your Need**: Service-based marketing visuals

### Step-by-Step Adaptation

#### 1. Update Data Model

**Before (Product):**
```python
@dataclass
class ProductProfile:
    product_name: str
    category: str
    features: List[str]
    price_range: str
```

**After (Service):**
```python
@dataclass
class ServiceProfile:
    business_name: str
    service_type: str  # "dental" | "vet" | "salon"
    key_services: List[str]
    team_members: List[Dict[str, str]]  # name, role, specialty
    accreditations: List[str]
    facility_features: List[str]
    target_demographic: str
    brand_values: List[str]
    location: Dict[str, str]  # city, neighborhood
    business_hours: str
    price_indication: str  # "affordable" | "mid-range" | "premium"
```

#### 2. Update Image Types

**Before:**
```python
class ImageType(Enum):
    MASTER_PRODUCT_SHOT = 1
    WHATS_IN_THE_BOX_FLAT_LAY = 2
    ...
```

**After:**
```python
class ServiceImageType(Enum):
    TEAM_PROFESSIONAL_PORTRAIT = 1
    FACILITY_INTERIOR_TOUR = 2
    BEFORE_AFTER_RESULTS = 3
    CUSTOMER_TESTIMONIAL_VISUAL = 4
    SERVICE_PROCESS_DEMONSTRATION = 5
    EQUIPMENT_TECHNOLOGY_SHOWCASE = 6
    COMMUNITY_ENGAGEMENT_PHOTO = 7
    SEASONAL_PROMOTION_BANNER = 8
    SAFETY_CLEANLINESS_HIGHLIGHT = 9
    CREDENTIALS_AWARDS_DISPLAY = 10
```

#### 3. Update Agent Prompts

**Product Interpreter → Service Interpreter**

**Before:**
```python
prompt = f"Analyze this product and extract features"
```

**After:**
```python
prompt = f"""
Analyze this {service_type} business information:

Business: {business_name}
Services: {services}
Team: {team_info}

Extract:
1. Core service offerings
2. Unique differentiators
3. Target patient/client demographics
4. Key trust factors (credentials, years in business)
5. Facility features (modern equipment, clean space)

Create a ServiceProfile in JSON format.
"""
```

#### 4. Customize Image Generation Prompts

**Dental Practice Example:**

```python
# For TEAM_PROFESSIONAL_PORTRAIT
prompt = f"""
Professional team photo for {business_name}, a modern dental practice.

Team composition:
{format_team_members(team)}

Setting:
- Clean, modern dental office
- Natural lighting with professional photography
- Team wearing professional dental attire
- Warm, welcoming expressions
- Background: subtle dental office elements

Style:
- Corporate professional but approachable
- High-quality medical photography standards
- Trust-building composition
- Diversity represented if applicable

Brand colors: {brand_colors}
"""

# For BEFORE_AFTER_RESULTS
prompt = f"""
Professional before/after dental treatment results showcase.

Requirements:
- Split-screen comparison layout
- Clinical photography standards
- Privacy-preserving (no full face if not authorized)
- Focus on treatment area
- Professional medical photography lighting
- HIPAA-compliant presentation

Treatment type: {treatment_type}
Results timeframe: {timeframe}

Style:
- Medical professional standard
- Clear documentation quality
- Patient consent verified visuals
"""

# For FACILITY_INTERIOR_TOUR
prompt = f"""
Modern dental practice interior photography.

Showcase:
- Reception area: welcoming, clean, organized
- Treatment rooms: state-of-the-art equipment
- Sterilization area: hygiene standards visible
- Technology: digital X-ray, modern tools
- Comfort features: patient amenities

Lighting:
- Natural light where possible
- Professional medical facility standards
- Bright, clean, inviting

Style:
- Real estate / healthcare facility photography
- Wide-angle for space perception
- Detail shots of technology
- Human element: staff or patients (with consent)
```

#### 5. Add Industry-Specific Validation

```python
class ServiceBusinessValidator:
    """Validates service business data"""
    
    @staticmethod
    def validate_dental_profile(profile: ServiceProfile) -> List[str]:
        """Check dental-specific requirements"""
        issues = []
        
        # Check required accreditations
        required_creds = ["DDS", "DMD", "ADA"]
        if not any(cred in profile.accreditations for cred in required_creds):
            issues.append("Missing dental credentials")
        
        # Check HIPAA compliance language
        if "hipaa" not in str(profile).lower():
            issues.append("Add HIPAA compliance note")
        
        # Check for common dental services
        common_services = ["cleaning", "exam", "x-ray"]
        if not any(s in str(profile.key_services).lower() for s in common_services):
            issues.append("Missing common dental services")
        
        return issues
    
    @staticmethod
    def validate_vet_profile(profile: ServiceProfile) -> List[str]:
        """Check veterinary-specific requirements"""
        issues = []
        
        # Check vet credentials
        if "DVM" not in str(profile.accreditations):
            issues.append("Missing DVM credential")
        
        # Check species served
        if not any(word in str(profile) for word in ["dog", "cat", "pet"]):
            issues.append("Specify species/animals served")
        
        return issues
```

#### 6. Create Industry-Specific Agents

```python
def _initialize_service_agents(self, service_type: str):
    """Initialize agents specialized for service businesses"""
    
    # Base configuration
    text_model = "gemini-2.0-flash-exp"
    
    # 1. Service Interpreter (replaces Product Interpreter)
    self.service_interpreter_agent = Agent(
        agent_name="Service-Business-Interpreter",
        agent_description=f"Analyzes {service_type} business information",
        model_name=text_model,
        system_prompt=self._get_service_interpreter_prompt(service_type),
        ...
    )
    
    # 2. Visual Strategy Agent (replaces Image Type Selector)
    self.visual_strategy_agent = Agent(
        agent_name="Service-Visual-Strategy",
        agent_description="Selects marketing visuals for service businesses",
        model_name=text_model,
        system_prompt=self._get_visual_strategy_prompt(service_type),
        ...
    )
    
    # 3. Compliance Checker Agent (NEW!)
    self.compliance_agent = Agent(
        agent_name="Healthcare-Compliance-Checker",
        agent_description="Ensures HIPAA and medical advertising compliance",
        model_name=text_model,
        system_prompt="""
        Review all marketing materials for:
        - HIPAA compliance
        - Patient privacy protection
        - Medical advertising regulations
        - State dental/veterinary board guidelines
        Flag any issues before generation.
        """,
        ...
    )
    
    # 4-6: Keep similar structure but customize prompts
```

#### 7. Add Before/After Image Processing

```python
class BeforeAfterImageGenerator:
    """Specialized generator for before/after visuals"""
    
    def __init__(self, compliance_agent: Agent):
        self.compliance_agent = compliance_agent
    
    def generate_before_after(
        self,
        before_image_path: str,
        after_image_path: str,
        treatment_info: Dict,
        patient_consent: bool = False
    ) -> str:
        """
        Generate before/after comparison image
        
        Args:
            before_image_path: Path to before image
            after_image_path: Path to after image
            treatment_info: Details about treatment
            patient_consent: MUST be True to proceed
        
        Returns:
            Path to generated comparison image
        """
        
        # Compliance check
        if not patient_consent:
            raise ValueError("Patient consent required for before/after images")
        
        # Check compliance
        compliance_check = self.compliance_agent.run(
            f"Review this before/after usage: {treatment_info}"
        )
        
        if "REJECT" in compliance_check:
            raise ValueError(f"Compliance issue: {compliance_check}")
        
        # Process images
        # (Use PIL or similar to create side-by-side comparison)
        ...
        
        return output_path
```

---

## 🔐 COMPLIANCE & SAFETY ADDITIONS

### For Healthcare/Service Businesses

```python
class HealthcareMarketingCompliance:
    """Ensures marketing materials meet healthcare regulations"""
    
    HIPAA_REQUIREMENTS = [
        "Patient consent obtained",
        "No personally identifiable information",
        "Medical records secured",
        "Authorization forms signed"
    ]
    
    ADVERTISING_GUIDELINES = [
        "No guarantees of results",
        "Realistic treatment expectations",
        "Licensed provider credentials",
        "Compliant testimonials only"
    ]
    
    @staticmethod
    def validate_before_generation(
        profile: ServiceProfile,
        image_type: ServiceImageType
    ) -> Tuple[bool, List[str]]:
        """
        Validate compliance BEFORE generating images
        
        Returns:
            (is_compliant, list_of_issues)
        """
        issues = []
        
        # Check for patient imagery
        if image_type in [
            ServiceImageType.BEFORE_AFTER_RESULTS,
            ServiceImageType.CUSTOMER_TESTIMONIAL_VISUAL
        ]:
            if not profile.patient_consent_verified:
                issues.append("Patient consent not verified")
        
        # Check credentials mentioned
        if image_type == ServiceImageType.CREDENTIALS_AWARDS_DISPLAY:
            if not profile.accreditations:
                issues.append("No credentials to display")
        
        # Check for false claims
        if "guaranteed" in str(profile).lower():
            issues.append("Cannot guarantee medical results")
        
        return (len(issues) == 0, issues)
```

---

## 🚀 INTEGRATION WITH YOUR EXISTING STACK

### 1. Voice Integration (Vapi)

```python
from vapi import VapiClient

class VoiceToMarketingPipeline:
    """Convert voice input to marketing visuals"""
    
    def __init__(self):
        self.vapi = VapiClient(api_key=os.getenv("VAPI_KEY"))
        self.agency = ProductMarketingAgency()
    
    async def handle_voice_request(self, call_id: str):
        """
        Process voice call and generate marketing materials
        
        Workflow:
        1. User calls and describes their business
        2. Vapi transcribes
        3. Extract business info
        4. Generate marketing visuals
        5. Send via SMS/email
        """
        
        # Get transcript
        transcript = await self.vapi.get_call_transcript(call_id)
        
        # Extract business info using Product Interpreter
        service_profile = self.agency.product_interpreter_agent.run(
            f"Extract service business information from: {transcript}"
        )
        
        # Generate visuals
        results = self.agency.run_marketing_campaign(
            product_data=service_profile,
            interactive=False
        )
        
        # Send results
        await self.send_results_via_sms(results)
        
        return results
```

### 2. Obsidian Knowledge Base Integration

```python
class ObsidianMarketingSync:
    """Sync marketing campaigns to Obsidian vault"""
    
    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.campaigns_dir = self.vault_path / "04_AI-Chats" / "Marketing-Campaigns"
    
    def save_campaign_note(self, profile: ServiceProfile, results: List[str]):
        """
        Save campaign as Obsidian markdown note
        
        Format:
        ---
        provider: Product-Marketing-Agency
        date: 2024-12-21
        business: Example Dental
        project: Marketing-Campaign
        tags: [marketing, dental, ai-generated]
        ---
        
        # Marketing Campaign: Example Dental
        
        ## Business Profile
        ...
        
        ## Generated Assets
        - [[image1.png]]
        - [[image2.png]]
        
        ## Results
        ...
        """
        
        # Create markdown
        note_content = self._format_campaign_markdown(profile, results)
        
        # Save to vault
        note_path = self.campaigns_dir / f"{profile.business_name}_{profile.timestamp}.md"
        note_path.write_text(note_content)
        
        # Copy images
        self._copy_images_to_vault(results)
```

### 3. Multi-LLM Orchestration

```python
class MultiLLMMarketingSystem:
    """Use different LLMs for different tasks"""
    
    def __init__(self):
        # Claude for strategy
        self.strategy_llm = "claude-3-sonnet"
        
        # Gemini for image generation
        self.image_llm = "gemini-2.5-flash-image-preview"
        
        # Local model for pre-processing
        self.local_llm = "llama-3-8b"
    
    def run_campaign(self, business_info: str):
        """
        Workflow:
        1. Local LLM: Clean and structure input
        2. Claude: Develop marketing strategy
        3. Gemini: Generate visuals
        4. Claude: Write copy for each visual
        """
        
        # Step 1: Pre-process with local model
        structured_data = self._preprocess_local(business_info)
        
        # Step 2: Strategy with Claude
        strategy = self._develop_strategy_claude(structured_data)
        
        # Step 3: Visuals with Gemini
        images = self._generate_images_gemini(strategy)
        
        # Step 4: Copy with Claude
        final_materials = self._write_copy_claude(images, strategy)
        
        return final_materials
```

---

## 📊 PERFORMANCE OPTIMIZATION

### Caching Strategy

```python
from functools import lru_cache
import hashlib

class CachedMarketingAgency(ProductMarketingAgency):
    """Add caching to avoid redundant generation"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cache = {}
    
    def _cache_key(self, profile: ServiceProfile, image_type: ImageType) -> str:
        """Generate cache key from profile + image type"""
        data = f"{profile.business_name}_{image_type.value}_{profile.timestamp}"
        return hashlib.md5(data.encode()).hexdigest()
    
    def generate_image_cached(self, profile, image_type):
        """Check cache before generating"""
        cache_key = self._cache_key(profile, image_type)
        
        if cache_key in self.cache:
            print(f"✅ Cache hit for {image_type.name}")
            return self.cache[cache_key]
        
        # Generate if not cached
        result = self._generate_marketing_image(profile, image_type)
        
        # Store in cache
        self.cache[cache_key] = result
        
        return result
```

### Batch Processing Optimization

```python
async def batch_generate_async(self, profiles: List[ServiceProfile]):
    """Generate campaigns in parallel"""
    
    import asyncio
    
    async def process_one(profile):
        return self.run_marketing_campaign(profile)
    
    # Process in parallel
    tasks = [process_one(p) for p in profiles]
    results = await asyncio.gather(*tasks)
    
    return results
```

---

## 🎓 KEY TAKEAWAYS

### Swarms Patterns You Now Understand

1. **Pipeline Pattern**: Sequential agent execution
2. **Fan-Out Pattern**: Parallel task spawning
3. **Coordinator Pattern**: Orchestrator manages workflow
4. **Transformer Pattern**: Unstructured → structured
5. **Generator Pattern**: Prompt → artifact
6. **Finalizer Pattern**: Cleanup and delivery

### Adaptation Principles

1. **Change Data Models**: ProductProfile → ServiceProfile
2. **Update Image Types**: Product-centric → Service-centric
3. **Customize Prompts**: Context matters
4. **Add Compliance**: Healthcare regulations
5. **Integrate Workflows**: Voice, knowledge base, multi-LLM

### Production Readiness

- [ ] Add authentication
- [ ] Implement caching
- [ ] Set up monitoring
- [ ] Add compliance checks
- [ ] Create backup strategy
- [ ] Configure CI/CD
- [ ] Cost tracking
- [ ] Error alerting

---

**Next Steps**:
1. Review this guide
2. Test the Product Marketing Agency
3. Start adapting for your service use case
4. Integrate with your existing stack
5. Deploy to production

---

**Questions? Check**:
- COMPLETE_SETUP_GUIDE.md
- QUICK_REFERENCE.md
- Official Swarms Docs: https://docs.swarms.world

**Last Updated**: Dec 21, 2024
