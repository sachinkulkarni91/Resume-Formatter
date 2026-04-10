# Deployment Guide

## Local Docker Deployment

### Prerequisites
- Docker Desktop installed
- Gemini API Key

### Quick Start

1. **Create .env file in project root:**
```bash
GEMINI_API_KEY=your_gemini_api_key_here
```

2. **Build and run with Docker Compose:**
```bash
docker-compose up --build
```

3. **Access:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000

### Scaling

To run multiple backend instances:
```bash
docker-compose up --build --scale backend=3
```

---

## Cloud Deployment Options

### Option 1: Railway (Recommended - Easiest)

**Backend Deployment:**
1. Push repository to GitHub
2. Go to [Railway](https://railway.app)
3. New Project → Import GitHub Repo
4. Add environment variables:
   - `GEMINI_API_KEY=your_key`
5. Deploy

**Frontend Deployment:**
1. Create .env:
   ```
   REACT_APP_API_URL=https://your-backend.railway.app
   ```
2. Deploy frontend to Railway

### Option 2: Heroku

**Backend:**
```bash
# Install Heroku CLI
# heroku login
heroku create resume-formatter-api
heroku buildpacks:add heroku/python
heroku config:set GEMINI_API_KEY=your_key
git push heroku main
```

**Frontend:**
```bash
# Use Vercel instead - better for React
npm install -g vercel
vercel
```

### Option 3: AWS (Advanced)

**Backend on EC2:**
```bash
# SSH into EC2 instance
ssh -i key.pem ec2-user@instance-ip

# Install Docker
sudo yum update -y
sudo yum install -y docker
sudo systemctl start docker

# Clone and run
git clone your-repo
cd Resume-Formatter
docker-compose up -d
```

**Frontend on S3 + CloudFront:**
```bash
npm run build
aws s3 sync dist/ s3://your-bucket/
# Create CloudFront distribution
```

### Option 4: Google Cloud Run

**Backend:**
```bash
# Build image
gcloud builds submit --tag gcr.io/PROJECT_ID/resume-formatter

# Deploy
gcloud run deploy resume-formatter \
  --image gcr.io/PROJECT_ID/resume-formatter \
  --platform managed \
  --set-env-vars GEMINI_API_KEY=your_key \
  --memory 2Gi \
  --timeout 300
```

---

## Environment Configuration

### Backend Environment Variables

```bash
# API Configuration
GEMINI_API_KEY=                    # Required: Your Gemini API key
API_HOST=0.0.0.0                  # Default
API_PORT=8000                     # Default
CORS_ORIGINS=*                    # Adjust for production

# File Upload Configuration (Optional)
MAX_FILE_SIZE=52428800            # 50MB
UPLOAD_DIR=uploads                # Temporary storage
OUTPUT_DIR=outputs                # Generated files
```

### Frontend Environment Variables

```bash
# API URL - Must point to backend
REACT_APP_API_URL=https://your-backend-url.com
```

---

## Production Checklist

- [ ] Set up HTTPS/SSL certificates
- [ ] Configure CORS properly (don't use * in production)
- [ ] Enable rate limiting on API
- [ ] Set up monitoring and logging
- [ ] Configure backup for outputs
- [ ] Test resume formatting thoroughly
- [ ] Set up CI/CD pipeline
- [ ] Monitor Gemini API costs
- [ ] Set up error tracking (Sentry)
- [ ] Configure CDN for static assets
- [ ] Enable request logging
- [ ] Set up database backups (if added)
- [ ] Test disaster recovery
- [ ] Document deployment process

---

## Monitoring

### Using PM2 (Alternative to Docker)

```bash
# Install PM2
npm install -g pm2

# Start backend
cd backend
pm2 start main.py --name "resume-backend" --interpreter python

# Start frontend
cd ../frontend
pm2 start "npm run dev" --name "resume-frontend"

# Monitor
pm2 monit

# Logs
pm2 logs
```

### Useful Monitoring Commands

```bash
# View all processes
pm2 list

# View logs
pm2 logs resume-backend

# Restart on crash
pm2 restart resume-backend

# Start on system boot
pm2 startup
pm2 save
```

---

## Performance Optimization

### Backend Optimization

1. **Enable Caching:**
```python
from functools import lru_cache

@lru_cache(maxsize=128)
def cached_extraction(file_hash):
    # Avoid re-parsing same files
    pass
```

2. **Use Connection Pooling:**
```python
# Update gemini_service.py to reuse connections
```

3. **Enable GZIP Compression:**
```python
from fastapi.middleware.gzip import GZIPMiddleware
app.add_middleware(GZIPMiddleware, minimum_size=1000)
```

### Frontend Optimization

1. **Code Splitting:**
```javascript
const App = lazy(() => import('./App'))
```

2. **Image Optimization:**
- Use modern formats (WebP)
- Lazy load images

3. **Bundle Analysis:**
```bash
npm run build -- --analyze
```

---

## Troubleshooting

### High Memory Usage
- Limit workers: `--workers 2`
- Reduce max file size
- Add swap space

### Slow API Response
- Check Gemini API rate limits
- Add caching layer
- Optimize file parsing

### SSL Certificate Issues
- Use Let's Encrypt (free)
- Update certificates before expiry
- Configure auto-renewal

### High Costs
- Monitor Gemini API usage
- Implement request caching
- Set rate limits per user

---

## Backup and Disaster Recovery

### Backup Strategy

1. **Database/Configuration:**
```bash
# Backup .env
cp backend/.env backup/.env.$(date +%s)

# Backup outputs
tar -czf backup/outputs-$(date +%Y%m%d).tar.gz backend/outputs/
```

2. **Automated Backups:**
```bash
# Create cron job
0 2 * * * /path/to/backup-script.sh
```

### Recovery Process

1. Restore from backup
2. Verify file integrity
3. Test with sample resume
4. Monitor logs for errors

---

## Security Best Practices

1. **API Security:**
   - Use HTTPS only
   - Implement rate limiting
   - Validate all inputs
   - Use API keys for sensitive endpoints

2. **File Security:**
   - Scan uploads for malware
   - Validate file types
   - Limit file size
   - Auto-delete old files

3. **Data Protection:**
   - Encrypt sensitive data
   - Use environment variables for secrets
   - Implement access logging
   - Regular security audits

4. **Dependency Security:**
```bash
# Check for vulnerabilities
pip audit
npm audit
```

---

## Cost Estimation

### Monthly Costs (Estimate)

| Service | Usage | Cost |
|---------|-------|------|
| Gemini API | 1000 requests | $1-5 |
| Hosting (Railway) | Small plan | $5-20 |
| Storage | 10GB | $0-1 |
| CDN | 1GB bandwidth | $0.20 |
| **Total** | | **$6-26** |

### Cost Optimization

- Use Railway/Vercel free tier for low traffic
- Implement caching to reduce API calls
- Compress input files
- Use spot instances for batch processing

---

## Support

For deployment issues:
1. Check logs: `docker logs resume-formatter-backend`
2. Verify .env configuration
3. Test Gemini API independently
4. Check firewall/port settings
5. Review application documentation

---

## Next Steps

1. Choose deployment platform
2. Set up CI/CD pipeline
3. Configure monitoring
4. Set up backups
5. Test end-to-end workflow
6. Deploy to production
7. Monitor performance
8. Gather user feedback

