# AWS Video Downloader System

A complete serverless video management system built on AWS with intelligent Lambda/Fargate routing, authentication, admin dashboard, and comprehensive video management capabilities.

## Features

### Core Functionality
- **Video Download**: Download videos from YouTube, Rumble, and other platforms
- **Video Upload**: Direct upload to S3 with automatic thumbnail generation
- **External Video Support**: Add YouTube, Rumble, and Facebook videos without downloading
- **Intelligent Routing**: Automatic Lambda/Fargate selection based on video length
- **Thumbnail Generation**: Automatic thumbnail creation for uploaded/downloaded videos

### Authentication & Authorization
- **JWT-based Authentication**: 24-hour token expiration
- **Three-tier Role System**: Super User > Admin > User hierarchy
- **Role-based Permissions**: Granular access control
- **User Management**: Create, edit, delete users with role restrictions

### Video Management
- **Ownership System**: Videos track owner email with transfer capabilities
- **Visibility Controls**: Public/Private video settings
- **Tag Management**: Comprehensive tagging with autocomplete
- **Search & Filter**: Advanced filtering by title, tags, visibility, owner
- **Embed Support**: Shareable embed links for public videos

### Admin Dashboard
- **User Management**: Full CRUD operations for user accounts
- **Video Management**: Edit metadata, change ownership, manage visibility
- **Tag Management**: Create, rename, delete tags with video associations
- **System Overview**: Statistics and monitoring
- **Download Status**: Real-time job tracking

## Architecture

### AWS Services Used
- **Lambda Functions**: Video processing, APIs, thumbnail generation
- **Fargate**: Heavy video processing tasks
- **S3**: Video and thumbnail storage
- **CloudFront**: CDN for fast content delivery
- **DynamoDB**: User data, video metadata, job tracking
- **API Gateway**: RESTful API endpoints
- **SNS**: Email notifications

### API Endpoints
- **Auth API**: User authentication and JWT management
- **Admin API**: Administrative operations and user management
- **TAG API**: Video metadata and tag management
- **Router API**: Download job routing and management
- **Video List API**: S3-based video listing

## Database Schema

### Users Table
- `user_id` (Primary Key)
- `email`, `password_hash`, `role`
- `created_at`, `updated_at`, `active`

### Video Metadata Table
- `video_id` (Primary Key)
- `filename`, `title`, `tags[]`
- `owner`, `visibility`
- `video_type`, `external_url`
- `upload_date`, `created_at`

### Download Jobs Table
- `job_id` (Primary Key)
- `status`, `progress`, `error_message`
- `created_at`, `updated_at`

## Deployment

### Prerequisites
- AWS CLI configured
- Python 3.9+ for Lambda functions
- S3 bucket for video storage
- CloudFront distribution

### Lambda Functions
1. **video-downloader**: Main video processing
2. **video-router**: Job routing logic
3. **video-tag-api**: Metadata management
4. **admin-api**: Administrative operations
5. **auth-api**: Authentication
6. **thumbnail-generator**: Thumbnail creation

### Frontend Files
- `index.html`: Landing page
- `login.html`: Authentication
- `videos.html`: Video gallery
- `admin.html`: Admin dashboard
- `embed.html`: Embedded video player
- `category.html`: Tag-based browsing
- `profile.html`: User profile management

## Configuration

### Environment Variables
- JWT_SECRET: Secret key for token signing
- S3_BUCKET: Video storage bucket name
- CLOUDFRONT_URL: CDN distribution URL

### Default Credentials
- **Super User**: super@admin.com / SuperSecure123!
- **Access URL**: https://d271vky579caz9.cloudfront.net

## Usage

### For Users
1. Register/Login to access videos
2. Browse videos by tags or search
3. View public videos and owned private videos
4. Share videos via embed links

### For Admins
1. Access admin dashboard
2. Manage users and roles
3. Upload/download videos
4. Edit video metadata and ownership
5. Manage tags and categories

### For Super Users
- All admin capabilities
- Create other super users
- System-wide access and control

## External Video Support

### Supported Platforms
- **YouTube**: Full embed support with proper video IDs
- **Rumble**: Embed support with video ID extraction
- **Facebook**: Basic embed support (may have restrictions)

### Adding External Videos
1. Use "Add External Video" in admin dashboard
2. Provide URL, title, tags, and visibility
3. System automatically detects platform type
4. Creates embed-ready entries without downloading

## Privacy & Security

### Video Visibility
- **Public**: Visible to all authenticated users
- **Private**: Only visible to owner and admins/super users

### Role Permissions
- **Users**: View public videos and own private videos
- **Admins**: Manage videos, users (except super users), tags
- **Super Users**: Full system access and control

## Troubleshooting

### Common Issues
1. **Facebook embeds not working**: Platform restrictions on embedding
2. **Thumbnail generation fails**: Check Lambda timeout settings
3. **Large video downloads fail**: Use Fargate option for long videos
4. **Authentication issues**: Check JWT token expiration (24 hours)

### Debug Features
- Console logging in browser developer tools
- Download status tracking page
- Error messages in admin dashboard

## Development

### Local Development
1. Clone repository
2. Configure AWS credentials
3. Deploy Lambda functions
4. Upload frontend files to S3
5. Configure CloudFront distribution

### Adding New Features
- Lambda functions in respective directories
- Frontend updates in HTML files
- Database schema changes in DynamoDB
- API endpoint additions in API Gateway

## License

This project is for educational and personal use.