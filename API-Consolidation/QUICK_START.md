# Quick Start Guide: API Consolidation

## 🎯 Goal
Consolidate 25 active API Gateways into 1 unified API with custom domain and automated CI/CD.

**Time Required**: 2 weeks (16 hours)
**Primary Value**: 4-6 hours/week time savings + professional architecture

---

## ⚡ Quick Start (Week 1)

### Prerequisites
- AWS CLI configured
- PowerShell 7+ or Bash
- Domain in Route 53: `christianconservativestoday.com`

### Step 1: Request SSL Certificate (5 minutes)

```bash
aws acm request-certificate \
  --domain-name api.christianconservativestoday.com \
  --validation-method DNS \
  --region us-east-1
```

**Action**: Add DNS validation records in Route 53 (AWS Console will show these)
**Wait**: 5-10 minutes for validation

### Step 2: Create Unified API (30 minutes)

```powershell
cd API-Consolidation\scripts
.\create-unified-api.ps1
```

This script will:
- ✅ Create REST API Gateway
- ✅ Create 17 base path resources
- ✅ Create proxy resources for each path
- ✅ Map all Lambda functions
- ✅ Enable CORS
- ✅ Deploy to production

**Output**: API ID saved to `api-id.txt`

### Step 3: Configure Custom Domain (10 minutes)

```powershell
.\configure-custom-domain.ps1 -CertificateArn YOUR_CERTIFICATE_ARN
```

**Wait**: 5-10 minutes for DNS propagation

### Step 4: Test Unified API (10 minutes)

```powershell
.\test-unified-api.ps1
```

Expected output: All tests pass ✅

### Step 5: Update Frontend URLs (30 minutes)

See `API_MAPPING.md` for URL mappings.

**Manual approach**: Update each HTML file
**Automated approach**: Use search & replace (see API_MAPPING.md)

---

## 🚀 Quick Start (Week 2)

### Step 1: Create GitHub Repository (10 minutes)

```bash
cd C:\Users\Ed\Documents\Programming\AWS\Downloader

git init
git add .
git commit -m "Initial commit"

# Create repo on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/christian-conservatives-today.git
git branch -M main
git push -u origin main
```

### Step 2: Configure AWS Secrets (5 minutes)

1. Go to GitHub → Settings → Secrets → Actions
2. Add these secrets:
   - `AWS_ACCESS_KEY_ID`
   - `AWS_SECRET_ACCESS_KEY`
   - `AWS_REGION` = `us-east-1`
   - `AWS_ACCOUNT_ID`

### Step 3: Copy Workflow Files (5 minutes)

```powershell
# Copy workflow files to main project
Copy-Item -Path "API-Consolidation\.github" -Destination ".." -Recurse -Force
```

### Step 4: Test GitHub Actions (10 minutes)

1. Go to GitHub → Actions tab
2. Select "Deploy All APIs"
3. Click "Run workflow"
4. Type "deploy-all" to confirm
5. Watch deployment progress

---

## 📋 Checklist

### Week 1: API Gateway Consolidation
- [ ] Request ACM certificate
- [ ] Validate certificate in Route 53
- [ ] Run `create-unified-api.ps1`
- [ ] Run `configure-custom-domain.ps1`
- [ ] Run `test-unified-api.ps1`
- [ ] Update frontend URLs
- [ ] Test website thoroughly
- [ ] Monitor CloudWatch logs

### Week 2: GitHub Actions CI/CD
- [ ] Create GitHub repository
- [ ] Push code to GitHub
- [ ] Configure AWS secrets
- [ ] Copy workflow files
- [ ] Test manual deployment
- [ ] Test automatic deployment (push code)
- [ ] Test rollback workflow
- [ ] Document deployment process

### Week 3: Cleanup
- [ ] Monitor new API for 1 week
- [ ] Verify all endpoints working
- [ ] Check CloudWatch metrics
- [ ] Delete old API Gateways
- [ ] Update documentation
- [ ] Celebrate cost savings! 🎉

---

## 🔧 Troubleshooting

### Issue: Certificate validation stuck
**Solution**: Check Route 53 for validation records, may take 10-15 minutes

### Issue: DNS not resolving
**Solution**: Wait 5-10 minutes for propagation, check with `nslookup api.christianconservativestoday.com`

### Issue: Lambda permission errors
**Solution**: Re-run `create-unified-api.ps1`, it will add permissions

### Issue: CORS errors
**Solution**: Check OPTIONS method is configured, re-run CORS section of script

### Issue: GitHub Actions fails
**Solution**: Verify AWS credentials in GitHub Secrets

---

## 📊 Expected Results

### Before
- 25 separate APIs
- Manual deployments (10 min each)
- Random AWS URLs
- Operational complexity
- Difficult to manage

### After
- 1 unified API
- Automated deployments (2 min)
- Custom domain: `api.christianconservativestoday.com`
- Clean architecture
- Easy to manage
- 4-6 hours/week time savings

---

## 🎯 Success Criteria

- [ ] All 17 services accessible via unified API
- [ ] Custom domain resolving correctly
- [ ] All tests passing
- [ ] Frontend working with new URLs
- [ ] GitHub Actions deploying successfully
- [ ] CloudWatch showing no errors
- [ ] Time savings realized (4-6 hours/week)

---

## 📚 Additional Resources

- `README.md` - Full overview
- `IMPLEMENTATION_GUIDE.md` - Detailed step-by-step
- `API_MAPPING.md` - URL mappings
- `GITHUB_ACTIONS_SETUP.md` - CI/CD details

---

## 🆘 Need Help?

1. Check CloudWatch logs for Lambda errors
2. Review `IMPLEMENTATION_GUIDE.md` for detailed steps
3. Test individual endpoints with curl/Postman
4. Check AWS Console for API Gateway configuration

---

**Ready to start?** Run `.\scripts\create-unified-api.ps1` to begin! 🚀
