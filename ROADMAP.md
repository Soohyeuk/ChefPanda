# ChefPanda Development Roadmap

## Supabase Integration

### Video Processing & Storage
- Store processed video data and transcripts in Supabase (PostgreSQL) during processing phase
- Maintain relationship between video data and generated recipes using foreign keys or references
- Implement unique identifiers to link video data with corresponding recipes
- Store metadata for efficient retrieval and analysis

### Recipe Generation & Storage
- Store AI-generated recipes in Supabase with references to source videos
- Implement versioning system for recipe variations
- Maintain data consistency between video and recipe tables
- Enable efficient recipe retrieval and updates

### Caching & Optimization
- Implement caching system to check for previously scraped videos (can use Supabase or in-memory cache)
- Avoid duplicate processing of already scraped content
- Optimize storage and retrieval operations
- Consider implementing TTL (time-to-live) for cache management if needed

## Recipe Retrieval System

### Section-Based Frontend Integration
- Implement modular recipe retrieval system for different frontend sections:
  - User trending recipes
  - Popular recipes
  - Cuisine-specific collections (e.g., Korean cuisine)
  - Other categorized sections
- Evaluate optimal API structure:
  - Single endpoint with categorized responses vs.
  - Multiple specialized endpoints per section

### ML Model Integration
- Integrate machine learning models for recipe categorization
- Options include:
  - Manual model development for specific needs
  - Integration of pre-built models
  - Hybrid approach combining multiple solutions
- Focus on accurate recipe categorization and recommendation

### API Design Considerations
- Determine optimal API structure for frontend needs
- Balance between:
  - Single comprehensive endpoint for all sections
  - Multiple specialized endpoints
- Consider typical usage patterns and frontend requirements
- Optimize for common request patterns

## Monetization Strategy

### Rate Limiting Implementation
- Implement basic rate limiting:
  - Limit scraping to 3 times per week (initial plan)
  - Track usage per client (store usage data in Supabase)
  - Implement rate limit checking logic

### Future Subscription Features
- Prepare for future subscription-based features:
  - Different rate limits based on subscription tier
  - Enhanced features for paid users
  - Flexible limit management system

### Premium Features
- Plan for premium feature implementation:
  - "Regenerate recipe by AI" feature for paid users
  - Additional premium features to be determined
- Note: User authentication and policy will be managed by Supabase

## Implementation Priorities

1. Supabase Integration
   - Essential for data persistence, authentication, and user policy
   - Foundation for all other features

2. Recipe Retrieval System
   - Core functionality for frontend
   - Initial ML model integration

3. Basic Rate Limiting
   - Implement basic usage restrictions
   - Prepare for future monetization

4. Premium Features
   - Develop after core functionality is stable
   - Not part of initial MVP

## Notes

- MVP will focus on core functionality with Supabase for all data and user management
- Monetization features will be implemented post-MVP
- ML model selection and integration strategy to be determined based on initial usage patterns
- API design will be optimized based on frontend requirements and usage patterns
- FastAPI server will interact with Supabase SQL for all CRUD and data operations

---
*This roadmap is a living document and will be updated as the project evolves.* 