# RFC: API Versioning Strategy

## Metadata

- **RFC ID**: RFC-0042
- **Author**: Engineering Team
- **Status**: Approved
- **Created**: 2024-11-15
- **Reviewers**: Platform Team, API Consumers

## Summary

Implement URL-based API versioning (e.g., `/api/v2/`) to enable breaking changes while maintaining backward compatibility. This replaces ad-hoc versioning approaches and establishes a standard deprecation policy of 12 months for major versions.

## Background

Our API has grown organically for 3 years without formal versioning. This causes:

1. **Breaking changes hit customers unexpectedly**: 47 customer complaints in past 6 months about API changes breaking integrations
2. **Developer velocity slowed**: Engineers spend 30% of API work on backward compatibility hacks instead of new features
3. **Technical debt accumulation**: 23 deprecated fields still in production because we can't remove them without versioning
4. **Inconsistent patterns**: Some endpoints use query params (`?version=2`), others use headers, most have no versioning

Recent data:

- 847 active API integrations across 312 customers
- 15 breaking changes deferred in backlog due to no versioning strategy
- $340K in engineering time spent on compatibility workarounds in past year

## Proposal

### Overview

Implement URL-based versioning with explicit deprecation lifecycle:

```
/api/v1/resources  <- Current (becomes deprecated)
/api/v2/resources  <- New version with breaking changes
```

### Versioning Rules

1. **Major versions** (`v1`, `v2`): Breaking changes allowed
2. **Minor versions**: Additive only, backward compatible
3. **Deprecation window**: 12 months from deprecation notice to removal
4. **Maximum concurrent versions**: 2 (current + previous)

### API Changes

```typescript
// Router structure
app.use('/api/v1', v1Router); // Legacy, deprecated
app.use('/api/v2', v2Router); // Current

// Version detection middleware
const apiVersion = (req: Request): number => {
  const match = req.path.match(/\/api\/v(\d+)\//);
  return match ? parseInt(match[1]) : 1;
};

// Response headers
res.setHeader('X-API-Version', '2');
res.setHeader('X-API-Deprecated', 'true'); // On v1 endpoints
res.setHeader('Deprecation', 'Sun, 01 Jun 2025 00:00:00 GMT');
```

### Database Changes

None required - versioning is at API layer only.

### Architecture

```
┌─────────────────────────────────────────────────┐
│                 API Gateway                      │
│  ┌──────────────────────────────────────────┐   │
│  │         Version Router                    │   │
│  │   /api/v1/* → v1 Controllers             │   │
│  │   /api/v2/* → v2 Controllers             │   │
│  └──────────────────────────────────────────┘   │
└─────────────────────────────────────────────────┘
                      │
         ┌────────────┼────────────┐
         ▼            ▼            ▼
    ┌─────────┐  ┌─────────┐  ┌─────────┐
    │ v1 Ctrl │  │ v2 Ctrl │  │ Shared  │
    │ (legacy)│  │ (new)   │  │ Service │
    └─────────┘  └─────────┘  └─────────┘
```

### Documentation Updates

- OpenAPI specs generated per version
- Migration guides for v1 → v2
- Deprecation notices in API docs
- SDK updates with version parameter

### Security Considerations

- Rate limiting applied per version (prevents v1 abuse during deprecation)
- Auth tokens valid across versions
- Audit logs include version number

## Alternatives Considered

### Alternative 1: Header-Based Versioning

**Description**: Version specified via `Accept: application/vnd.api.v2+json` header.

**Pros**:

- Cleaner URLs
- RESTful purists prefer this
- Version can be optional (default to latest)

**Cons**:

- Harder to test (need custom headers)
- Not visible in logs without custom parsing
- Breaks browser testing
- Many API tools don't support custom headers well

**Why not**: Developer experience is significantly worse. Our API is used by many non-technical integrators who struggle with header configuration.

### Alternative 2: Query Parameter Versioning

**Description**: Version via `?version=2` query parameter.

**Pros**:

- Easy to test in browser
- Visible in URLs
- Can default to latest if omitted

**Cons**:

- Pollutes query string
- Inconsistent with resource-based URL design
- Caching complications
- Easy to forget, causing unexpected behavior

**Why not**: Query params should be for filtering/pagination, not fundamental API behavior. Also creates caching headaches with CDN.

### Alternative 3: No Explicit Versioning (Additive Only)

**Description**: Never make breaking changes; only add fields/endpoints.

**Pros**:

- No migration burden on customers
- Simpler architecture
- GraphQL-like flexibility

**Cons**:

- Technical debt accumulates forever
- Can't fix fundamental design mistakes
- Response payloads bloat over time
- Performance degrades as we support all historical patterns

**Why not**: We already have 23 deprecated fields we can't remove. This approach is unsustainable long-term.

## Migration Plan

### Phase 1: Infrastructure (Week 1-2)

- [ ] Add version router middleware
- [ ] Create v2 controller scaffolding
- [ ] Add deprecation headers to v1
- [ ] Update logging to include version
- **Rollback**: Remove middleware, revert to single router

### Phase 2: Documentation (Week 2-3)

- [ ] Generate v2 OpenAPI spec
- [ ] Create migration guide
- [ ] Update SDK with version parameter
- [ ] Add deprecation notices to v1 docs
- **Rollback**: Revert documentation (no code impact)

### Phase 3: Customer Communication (Week 3-4)

- [ ] Email all API consumers about v2
- [ ] Add in-app notification for API users
- [ ] Publish blog post on versioning strategy
- **Rollback**: N/A (communication only)

### Phase 4: v1 Deprecation (Month 3)

- [ ] Log v1 usage metrics weekly
- [ ] Reach out to high-volume v1 users
- [ ] Add warning responses on v1 endpoints
- **Rollback**: Remove warning responses

### Phase 5: v1 Sunset (Month 12)

- [ ] Final deprecation notice (30 days)
- [ ] v1 returns 410 Gone
- [ ] Remove v1 code
- **Rollback**: Re-enable v1 from backup branch

### Feature Flags

- `api_v2_enabled`: Master switch for v2 endpoints
- `api_v1_deprecation_warning`: Show deprecation in v1 responses

### Backward Compatibility

- v1 remains fully functional for 12 months
- v1 receives security fixes only (no features)
- Migration tooling provided for common patterns

## Risks

| Risk                                         | Probability | Impact | Mitigation                                                              |
| -------------------------------------------- | ----------- | ------ | ----------------------------------------------------------------------- |
| Customer integrations break during migration | Medium      | High   | 12-month deprecation window, proactive outreach to top 50 API consumers |
| Version sprawl (too many versions)           | Low         | Medium | Policy: max 2 concurrent versions                                       |
| Performance overhead from version routing    | Low         | Low    | Benchmark shows <1ms overhead; cache version detection                  |
| SDK adoption lag                             | Medium      | Medium | Auto-update SDKs, provide migration scripts                             |

## Success Metrics

| Metric                              | Current | Target     | Measurement                           |
| ----------------------------------- | ------- | ---------- | ------------------------------------- |
| Breaking change customer complaints | 47/6mo  | <5/6mo     | Zendesk tickets tagged 'api-breaking' |
| Engineering time on compatibility   | 30%     | <10%       | Sprint tracking                       |
| v2 adoption rate                    | N/A     | 80% in 6mo | API logs                              |
| Deprecated field count              | 23      | 0          | Code audit                            |

## Open Questions

- [x] Should we support v1 and v2 in same SDK or separate packages? **Decision: Same SDK with version parameter**
- [ ] What's the SLA for v1 during deprecation period? (security fixes only, or bug fixes too?)
- [ ] Should we charge for v1 access after deprecation to encourage migration?

## References

- [Stripe API Versioning](https://stripe.com/docs/api/versioning) - Inspiration for approach
- [Microsoft REST API Guidelines](https://github.com/microsoft/api-guidelines)
- Internal doc: API Consumer Analysis (847 integrations)
