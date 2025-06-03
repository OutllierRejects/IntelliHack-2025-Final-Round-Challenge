# Troubleshooting Guide

Common issues and solutions for the Disaster Response Coordination System.

## 🚨 Emergency Issues

### System Down During Emergency

If the system is unavailable during an active emergency:

1. **Call 911 Immediately** for life-threatening situations
2. **Use backup hotline**: [Emergency Phone Number]
3. **Contact local emergency services** directly
4. **Try alternative access methods**:
   - SMS gateway: Text "HELP" to [SMS Number]
   - Email: emergency@disaster-response.com
   - Radio networks: Monitor emergency frequencies

## 🔧 Common Technical Issues

### Login and Authentication Problems

#### Can't Log In

**Symptoms**: Invalid credentials, login page not loading, session expired

**Solutions**:

1. **Check credentials**:

   ```bash
   # Verify email format
   user@example.com ✅
   user@example ❌

   # Check password requirements
   - Minimum 8 characters
   - Contains letters and numbers
   ```

2. **Clear browser cache**:

   ```bash
   # Chrome/Edge
   Ctrl+Shift+Delete → Clear browsing data

   # Firefox
   Ctrl+Shift+Delete → Clear cache
   ```

3. **Try incognito/private mode**:

   - Chrome: Ctrl+Shift+N
   - Firefox: Ctrl+Shift+P
   - Edge: Ctrl+Shift+N

4. **Reset password**:
   - Click "Forgot Password" on login page
   - Check email for reset link
   - Create new secure password

#### Session Keeps Expiring

**Symptoms**: Logged out frequently, "session expired" messages

**Solutions**:

1. **Check browser settings**:

   - Enable cookies for the site
   - Disable ad blockers temporarily
   - Allow JavaScript execution

2. **Update browser**:

   - Use latest version of Chrome, Firefox, or Edge
   - Clear old browser data

3. **Network connectivity**:
   - Check internet connection stability
   - Try different network if possible

#### Two-Factor Authentication Issues

**Symptoms**: Not receiving 2FA codes, codes not working

**Solutions**:

1. **Check phone/email**:

   - Verify correct phone number in profile
   - Check spam folder for emails
   - Ensure phone has cellular signal

2. **Time synchronization**:

   - Ensure device time is accurate
   - Sync with network time

3. **Backup codes**:
   - Use backup authentication codes
   - Contact support for assistance

### Application Performance Issues

#### Slow Loading

**Symptoms**: Pages take long to load, timeouts

**Solutions**:

1. **Check internet speed**:

   ```bash
   # Test connection speed
   speedtest-cli
   # or visit speedtest.net
   ```

2. **Reduce browser load**:

   - Close unnecessary tabs
   - Disable browser extensions
   - Clear cache and cookies

3. **Optimize settings**:
   - Reduce image quality in uploads
   - Limit concurrent operations
   - Use smaller file sizes

#### Features Not Working

**Symptoms**: Buttons not responding, forms not submitting

**Solutions**:

1. **JavaScript enabled**:

   - Check browser settings
   - Allow scripts for the site
   - Disable script blockers

2. **Browser compatibility**:

   ```
   ✅ Supported Browsers:
   - Chrome 90+
   - Firefox 88+
   - Safari 14+
   - Edge 90+
   ```

3. **Console errors**:
   ```bash
   # Check browser console
   F12 → Console tab
   # Look for red error messages
   ```

### Mobile App Issues

#### App Won't Start

**Solutions**:

1. **Restart app**:

   - Force close application
   - Clear app cache
   - Restart device

2. **Update app**:

   - Check app store for updates
   - Ensure iOS 14+ or Android 8+
   - Free up device storage

3. **Reinstall app**:
   - Uninstall current version
   - Download latest from app store
   - Login with existing account

#### GPS/Location Issues

**Symptoms**: Location not detected, inaccurate positioning

**Solutions**:

1. **Permission settings**:

   - Allow location access for app
   - Enable high accuracy mode
   - Check privacy settings

2. **GPS signal**:

   - Move to open area
   - Wait for GPS to acquire signal
   - Check if location services enabled

3. **Manual location entry**:
   - Enter address manually
   - Use what3words codes
   - Share location via maps app

## 🔐 Security and Privacy Issues

### Account Security

#### Suspected Account Compromise

**Signs**: Unexpected logins, changed information, unknown activity

**Immediate Actions**:

1. **Change password immediately**
2. **Review account activity log**
3. **Check personal information** for changes
4. **Enable two-factor authentication**
5. **Contact support** if suspicious activity found

#### Privacy Concerns

**Location Privacy**:

- Location only shared during active requests
- Data encrypted in transit and storage
- Location history can be deleted

**Communication Privacy**:

- Messages encrypted between users
- Personal information protected
- Communication logs can be requested

### Data Protection

#### Request Data Deletion

To delete your account and data:

1. **Login to account**
2. **Go to Privacy Settings**
3. **Select "Delete Account"**
4. **Confirm deletion request**
5. **Data removed within 30 days**

#### Export Personal Data

To export your data:

1. **Account Settings → Privacy**
2. **Select "Export Data"**
3. **Choose data categories**
4. **Receive download link via email**

## 🌐 Network and Connectivity Issues

### Internet Connection Problems

#### No Internet Access

**Solutions**:

1. **Check connection**:

   ```bash
   # Test connectivity
   ping google.com
   # or
   nslookup disaster-response.com
   ```

2. **Router issues**:

   - Restart router/modem
   - Check cable connections
   - Contact ISP if persistent

3. **Use mobile data**:
   - Switch to cellular network
   - Create mobile hotspot
   - Use public WiFi (secured)

#### Firewall/Proxy Issues

**Symptoms**: Can't access system from work/school networks

**Solutions**:

1. **Check firewall settings**:

   - Whitelist disaster-response.com
   - Allow ports 80, 443, 8000, 3000
   - Contact IT administrator

2. **Proxy configuration**:
   - Configure browser proxy settings
   - Use VPN if allowed
   - Access via mobile network

### WebSocket Connection Issues

**Symptoms**: Real-time updates not working, messages delayed

**Solutions**:

1. **Network configuration**:

   - Allow WebSocket connections
   - Check corporate firewall
   - Verify proxy settings

2. **Browser settings**:
   - Enable WebSockets in browser
   - Clear browser cache
   - Try different browser

## 🤖 AI and Processing Issues

### AI Agents Not Responding

**Symptoms**: Requests stuck in "processing", no AI analysis

**Solutions**:

1. **Check system status**:

   - Visit status page
   - Check service health
   - Review error messages

2. **Wait and retry**:

   - AI processing may take 2-5 minutes
   - High load can cause delays
   - System will retry automatically

3. **Manual processing**:
   - Contact administrator
   - Request manual review
   - Use emergency escalation

### Incorrect AI Classifications

**Symptoms**: Wrong priority assigned, poor matching

**Solutions**:

1. **Provide feedback**:

   - Rate AI accuracy
   - Report incorrect classifications
   - Suggest improvements

2. **Add more details**:

   - Include specific keywords
   - Provide clearer descriptions
   - Add relevant photos

3. **Manual override**:
   - Request human review
   - Update priority manually
   - Contact supervisor

## 📱 Role-Specific Issues

### Affected Individuals

#### Request Not Processed

**Symptoms**: Request stuck in submitted status

**Checklist**:

- [ ] All required fields completed
- [ ] Valid location provided
- [ ] Contact information correct
- [ ] Urgency level appropriate
- [ ] Photos uploaded successfully

**Actions**:

1. **Check request status** in dashboard
2. **Update missing information**
3. **Contact emergency hotline** if urgent
4. **Submit new request** if needed

#### Can't Contact Responder

**Solutions**:

1. **Use in-app messaging** first
2. **Call emergency contact** if provided
3. **Update request status** with new information
4. **Contact system dispatch**

### Volunteers

#### No Tasks Available

**Possible Causes**:

- All tasks assigned
- Location outside service area
- Skills don't match current needs
- Time restrictions

**Solutions**:

1. **Expand search radius**
2. **Update skill profile**
3. **Check availability settings**
4. **Consider different task types**

#### Task Assignment Issues

**Can't Accept Task**:

- Task may have been assigned to someone else
- Your profile may not meet requirements
- Check internet connectivity
- Refresh task list

**Incorrect Task Match**:

- Update skill profile
- Set location preferences
- Adjust availability schedule
- Provide feedback to improve matching

### First Responders

#### Coordination Problems

**Communication Issues**:

- Check radio frequencies
- Verify contact information
- Use backup communication methods
- Contact incident commander

**Resource Conflicts**:

- Check resource allocation system
- Contact logistics coordinator
- Report equipment issues
- Request additional resources

### Administrators

#### Dashboard Not Loading

**Solutions**:

1. **Check administrator permissions**
2. **Clear browser cache completely**
3. **Try different browser**
4. **Contact system administrator**

#### Data Inconsistencies

**Symptoms**: Reports show conflicting information

**Actions**:

1. **Check data source filters**
2. **Verify time range settings**
3. **Refresh data connections**
4. **Run data integrity checks**

## 🐳 Docker and Development Issues

### Docker Container Issues

#### Containers Won't Start

**Check container status**:

```bash
docker-compose ps
docker-compose logs [service_name]
```

**Common solutions**:

```bash
# Restart containers
docker-compose restart

# Rebuild containers
docker-compose build --no-cache
docker-compose up -d

# Clean and restart
make docker-clean
make docker-up
```

#### Port Conflicts

**Symptoms**: "Port already in use" errors

**Find conflicting processes**:

```bash
# Check port usage
lsof -i :3000
lsof -i :8000
netstat -tulpn | grep :3000
```

**Solutions**:

```bash
# Kill conflicting process
sudo kill -9 [PID]

# Change ports in docker-compose.yml
ports:
  - "3001:3000"  # Use port 3001 instead
```

#### Database Connection Issues

**Symptoms**: "Connection refused" to PostgreSQL

**Solutions**:

```bash
# Check database container
docker-compose logs postgres

# Reset database
make db-reset

# Check database connectivity
docker-compose exec postgres psql -U postgres -c "\l"
```

### Environment Configuration Issues

#### Missing Environment Variables

**Symptoms**: Application errors about missing config

**Check environment file**:

```bash
# Verify .env file exists
ls -la ai_services/.env

# Check required variables
grep -E "OPENAI_API_KEY|DATABASE_URL|JWT_SECRET" ai_services/.env
```

**Fix missing variables**:

```bash
# Copy template
cp ai_services/.env.example ai_services/.env

# Add missing variables
echo "OPENAI_API_KEY=your-key-here" >> ai_services/.env
```

#### API Key Issues

**OpenAI API Problems**:

```bash
# Test API key
curl -H "Authorization: Bearer $OPENAI_API_KEY" \
     https://api.openai.com/v1/models

# Check quota
curl -H "Authorization: Bearer $OPENAI_API_KEY" \
     https://api.openai.com/v1/usage
```

## 📊 Performance Optimization

### Database Performance

#### Slow Queries

**Identify slow queries**:

```sql
-- PostgreSQL slow query log
SELECT query, mean_time, calls
FROM pg_stat_statements
ORDER BY mean_time DESC
LIMIT 10;
```

**Optimize database**:

```bash
# Vacuum and analyze
docker-compose exec postgres psql -U postgres -d disaster_response -c "VACUUM ANALYZE;"

# Check indexes
docker-compose exec postgres psql -U postgres -d disaster_response -c "\di"
```

### Memory Issues

#### High Memory Usage

**Check container memory**:

```bash
docker stats
docker-compose exec api free -h
```

**Optimize memory usage**:

```bash
# Restart services
docker-compose restart api

# Adjust container limits in docker-compose.yml
deploy:
  resources:
    limits:
      memory: 1G
```

### API Performance

#### Slow API Responses

**Check API logs**:

```bash
docker-compose logs api | grep "ERROR\|WARNING"
```

**Performance monitoring**:

```bash
# Check response times
curl -w "@curl-format.txt" -o /dev/null -s http://localhost:8000/health

# Monitor with top
docker-compose exec api top
```

## 📞 Getting Additional Help

### Support Channels

| Issue Type      | Contact Method      | Response Time |
| --------------- | ------------------- | ------------- |
| Emergency       | Emergency Hotline   | Immediate     |
| System Down     | Status Page + Email | 15 minutes    |
| Critical Bug    | Support Ticket      | 2 hours       |
| General Issue   | Email Support       | 24 hours      |
| Feature Request | Community Forum     | 1 week        |

### Information to Include

When contacting support, provide:

1. **User Information**:

   - User ID or email
   - Role (affected individual, volunteer, etc.)
   - Account creation date

2. **Technical Details**:

   - Browser/app version
   - Operating system
   - Device type
   - Internet connection type

3. **Error Information**:

   - Exact error messages
   - Steps to reproduce
   - Screenshots/screen recordings
   - Console errors (F12 → Console)

4. **Impact Assessment**:
   - Urgency level
   - Number of people affected
   - Workaround attempts
   - Business impact

### Self-Help Resources

**Documentation**:

- [User Guides](user-guides/affected-individuals.md)
- [API Documentation](api/authentication.md)
- [Setup Guides](getting-started/quick-setup.md)

**Community**:

- User forums
- FAQ database
- Video tutorials
- Community wiki

**Status and Updates**:

- System status page
- Maintenance announcements
- Release notes
- Service updates

---

## 🔄 Feedback and Improvement

Help us improve the system by:

- Reporting bugs and issues
- Suggesting feature improvements
- Sharing success stories
- Participating in user surveys
- Contributing to documentation

**Feedback Channels**:

- In-app feedback forms
- Support email
- Community forums
- User surveys
- GitHub issues (for developers)

---

_Still need help? Contact our 24/7 support team or check the [community forums](https://community.disaster-response.com) for additional assistance._
