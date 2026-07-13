# Implementation Plan - AI Incident Response Platform

## Phase 1: Database Schema Migration
- [ ] Add user_id column to incidents table
- [ ] Add website_id column to incidents table  
- [ ] Add monitoring columns to websites table (slow_threshold, request_timeout, current_status, status_code, response_time_seconds, last_error, last_checked_at, updated_at)
- [ ] Create proper foreign keys

## Phase 2: Backend API Rewrites
- [ ] Rewrite incident_service.py (user_id, website_id support, proper CRUD)
- [ ] Add missing website APIs (PUT, DELETE, PATCH toggle, POST check)
- [ ] Add missing incident APIs (GET /incidents with filters, PATCH resolve, GET single)
- [ ] Add 401 Axios interceptor on frontend
- [ ] Fix Flask debug=False in production

## Phase 3: Multi-Website Monitoring
- [ ] Rewrite website_workflow.py to load websites from DB
- [ ] Rewrite scheduler_service.py to monitor per-website
- [ ] Fix settings.py - remove global MONITOR_URL pat

## Phase 4: Frontend Fixes
- [ ] Fix Dashboard to show user-specific data
- [ ] Fix Incidents page for proper filtering
- [ ] Add edit/delete/toggle website buttons to Websites page
- [ ] Add proper loading states and error handling

## Phase 5: Cleanup & Testing
- [ ] Remove obsolete global state code
- [ ] Add pytest tests
- [ ] Fix Docker setup
- [ ] Update README
- [ ] Test all flows