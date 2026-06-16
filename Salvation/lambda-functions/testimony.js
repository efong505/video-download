const { DynamoDBClient } = require('@aws-sdk/client-dynamodb');
const { DynamoDBDocumentClient, PutCommand, QueryCommand, GetCommand, UpdateCommand, DeleteCommand, ScanCommand } = require('@aws-sdk/lib-dynamodb');
const crypto = require('crypto');

const client = new DynamoDBClient({ region: 'us-east-1' });
const dynamodb = DynamoDBDocumentClient.from(client);

function generateId() {
    return crypto.randomBytes(8).toString('hex');
}

exports.handler = async (event) => {
    const { httpMethod, path, body, pathParameters } = event;
    const data = body ? JSON.parse(body) : {};
    
    try {
        if (httpMethod === 'GET' && path.startsWith('/testimony/')) {
            const testimonyId = pathParameters?.id || path.split('/').pop();
            return await getPublicTestimony(testimonyId);
        }
        
        switch (`${httpMethod} ${path}`) {
            case 'OPTIONS /testimonies':
                return {
                    statusCode: 200,
                    headers: {
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Headers': 'Content-Type,User-Email',
                        'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS'
                    },
                    body: ''
                };
            case 'GET /testimonies':
                const userEmail = event.queryStringParameters?.userEmail;
                return await getUserTestimonies(userEmail);
            case 'GET /testimonies/public':
                return await getPublicTestimonies();
            case 'OPTIONS /testimonies/public':
                return {
                    statusCode: 200,
                    headers: {
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Headers': 'Content-Type',
                        'Access-Control-Allow-Methods': 'GET,OPTIONS'
                    },
                    body: ''
                };
            case 'POST /testimonies':
                return await createTestimony(data);
            case 'PUT /testimonies':
                return await updateTestimony(data);
            case 'PUT /testimonies/visibility':
                return await updateTestimonyVisibility(data);
            case 'OPTIONS /testimonies/visibility':
                return {
                    statusCode: 200,
                    headers: {
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Headers': 'Content-Type',
                        'Access-Control-Allow-Methods': 'PUT,OPTIONS'
                    },
                    body: ''
                };
            case 'DELETE /testimonies':
                const testimonyId = event.queryStringParameters?.testimonyId;
                const deleteUserEmail = event.queryStringParameters?.userEmail;
                return await deleteTestimony(testimonyId, deleteUserEmail);
            case 'POST /share-email':
                return await shareTestimony(data);
            case 'POST /share-testimony':
                return await shareTestimonyWithFriend(data);
            case 'OPTIONS /share-testimony':
                return {
                    statusCode: 200,
                    headers: {
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Headers': 'Content-Type',
                        'Access-Control-Allow-Methods': 'POST,OPTIONS'
                    },
                    body: ''
                };
            default:
                return { statusCode: 404, body: JSON.stringify({ error: 'Not found' }) };
        }
    } catch (error) {
        return { 
            statusCode: 500,
            headers: {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type,User-Email',
                'Access-Control-Allow-Methods': 'GET,POST,OPTIONS'
            },
            body: JSON.stringify({ error: error.message }) 
        };
    }
};

async function createTestimony(data) {
    const { userEmail, title, content, visualTheme } = data;
    
    // Check user account status first
    const userResult = await dynamodb.send(new GetCommand({
        TableName: 'testimony-users',
        Key: { email: userEmail }
    }));
    
    if (!userResult.Item) {
        return {
            statusCode: 404,
            headers: {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type,User-Email',
                'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS'
            },
            body: JSON.stringify({ error: 'User not found' })
        };
    }
    
    const accountStatus = userResult.Item.accountStatus || 'active';
    if (accountStatus === 'suspended') {
        return {
            statusCode: 403,
            headers: {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type,User-Email',
                'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS'
            },
            body: JSON.stringify({ 
                error: 'Account suspended',
                message: 'Your account has been suspended. You cannot create testimonies.'
            })
        };
    }
    
    if (accountStatus === 'flagged') {
        return {
            statusCode: 403,
            headers: {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type,User-Email',
                'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS'
            },
            body: JSON.stringify({ 
                error: 'Account under review',
                message: 'Your account is under review. You cannot create testimonies at this time.'
            })
        };
    }
    
    // Content moderation check
    const moderationResult = await moderateContent(title, content);
    if (!moderationResult.approved) {
        // Flag user account for review
        await flagUserAccount(userEmail, moderationResult.reason, { title, content });
        
        return {
            statusCode: 400,
            headers: {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type,User-Email',
                'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS'
            },
            body: JSON.stringify({ 
                error: 'Content does not meet community guidelines. Account flagged for review.',
                reason: moderationResult.reason
            })
        };
    }
    
    const testimonyId = generateId();
    
    await dynamodb.send(new PutCommand({
        TableName: 'testimonies',
        Item: {
            testimonyId,
            userEmail,
            title,
            content,
            visualTheme: visualTheme || 'classic',
            isPublic: true,
            createdAt: new Date().toISOString(),
            sharedCount: 0
        }
    }));
    
    return { 
        statusCode: 201,
        headers: {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type,User-Email',
            'Access-Control-Allow-Methods': 'GET,POST,OPTIONS'
        },
        body: JSON.stringify({ 
            message: 'Testimony created successfully',
            testimonyId,
            shareUrl: `https://mytestimony.click/share/${testimonyId}`
        }) 
    };
}

async function getUserTestimonies(userEmail) {
    if (!userEmail) {
        return { 
            statusCode: 400,
            headers: {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type,User-Email',
                'Access-Control-Allow-Methods': 'GET,POST,OPTIONS'
            },
            body: JSON.stringify({ error: 'User email is required' }) 
        };
    }
    
    const result = await dynamodb.send(new QueryCommand({
        TableName: 'testimonies',
        IndexName: 'UserEmailIndex',
        KeyConditionExpression: 'userEmail = :email',
        ExpressionAttributeValues: { ':email': userEmail }
    }));
    
    return { 
        statusCode: 200,
        headers: {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type,User-Email',
            'Access-Control-Allow-Methods': 'GET,POST,OPTIONS'
        },
        body: JSON.stringify({ testimonies: result.Items }) 
    };
}

async function getPublicTestimony(testimonyId) {
    const result = await dynamodb.send(new GetCommand({
        TableName: 'testimonies',
        Key: { testimonyId }
    }));
    
    if (!result.Item || !result.Item.isPublic) {
        return { 
            statusCode: 404,
            headers: {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type,User-Email',
                'Access-Control-Allow-Methods': 'GET,POST,OPTIONS'
            },
            body: JSON.stringify({ error: 'Testimony not found' }) 
        };
    }
    
    // Get author name
    try {
        const userResult = await dynamodb.send(new GetCommand({
            TableName: 'testimony-users',
            Key: { email: result.Item.userEmail }
        }));
        result.Item.authorName = userResult.Item?.name || 'Anonymous';
    } catch {
        result.Item.authorName = 'Anonymous';
    }
    
    return { 
        statusCode: 200,
        headers: {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type,User-Email',
            'Access-Control-Allow-Methods': 'GET,POST,OPTIONS'
        },
        body: JSON.stringify({ testimony: result.Item }) 
    };
}

async function updateTestimony(data) {
    const { testimonyId, userEmail, title, content } = data;
    
    // Check user account status first
    const userResult = await dynamodb.send(new GetCommand({
        TableName: 'testimony-users',
        Key: { email: userEmail }
    }));
    
    if (!userResult.Item) {
        return {
            statusCode: 404,
            headers: {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type,User-Email',
                'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS'
            },
            body: JSON.stringify({ error: 'User not found' })
        };
    }
    
    const accountStatus = userResult.Item.accountStatus || 'active';
    if (accountStatus === 'suspended') {
        return {
            statusCode: 403,
            headers: {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type,User-Email',
                'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS'
            },
            body: JSON.stringify({ 
                error: 'Account suspended',
                message: 'Your account has been suspended. You cannot edit testimonies.'
            })
        };
    }
    
    if (accountStatus === 'flagged') {
        return {
            statusCode: 403,
            headers: {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type,User-Email',
                'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS'
            },
            body: JSON.stringify({ 
                error: 'Account under review',
                message: 'Your account is under review. You cannot edit testimonies at this time.'
            })
        };
    }
    
    // Content moderation check for updates
    const moderationResult = await moderateContent(title, content);
    if (!moderationResult.approved) {
        await flagUserAccount(userEmail, moderationResult.reason, { title, content });
        
        return {
            statusCode: 400,
            headers: {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type,User-Email',
                'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS'
            },
            body: JSON.stringify({ 
                error: 'Content does not meet community guidelines. Account flagged for review.',
                reason: moderationResult.reason
            })
        };
    }
    
    if (!testimonyId || !userEmail || !title || !content) {
        return { 
            statusCode: 400,
            headers: {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type,User-Email',
                'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS'
            },
            body: JSON.stringify({ error: 'Missing required fields' }) 
        };
    }
    
    await dynamodb.send(new UpdateCommand({
        TableName: 'testimonies',
        Key: { testimonyId },
        UpdateExpression: 'SET title = :title, content = :content',
        ConditionExpression: 'userEmail = :userEmail',
        ExpressionAttributeValues: { 
            ':title': title,
            ':content': content,
            ':userEmail': userEmail
        }
    }));
    
    return { 
        statusCode: 200,
        headers: {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type,User-Email',
            'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS'
        },
        body: JSON.stringify({ message: 'Testimony updated successfully' }) 
    };
}

async function deleteTestimony(testimonyId, userEmail) {
    if (!testimonyId || !userEmail) {
        return { 
            statusCode: 400,
            headers: {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type,User-Email',
                'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS'
            },
            body: JSON.stringify({ error: 'Missing testimonyId or userEmail' }) 
        };
    }
    
    await dynamodb.send(new DeleteCommand({
        TableName: 'testimonies',
        Key: { testimonyId },
        ConditionExpression: 'userEmail = :userEmail',
        ExpressionAttributeValues: { ':userEmail': userEmail }
    }));
    
    return { 
        statusCode: 200,
        headers: {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type,User-Email',
            'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS'
        },
        body: JSON.stringify({ message: 'Testimony deleted successfully' }) 
    };
}

async function getPublicTestimonies() {
    const result = await dynamodb.send(new ScanCommand({
        TableName: 'testimonies',
        FilterExpression: 'isPublic = :isPublic',
        ExpressionAttributeValues: { ':isPublic': true }
    }));
    
    // Get user names for testimonies
    const testimoniesWithNames = await Promise.all(
        (result.Items || []).map(async (testimony) => {
            try {
                const userResult = await dynamodb.send(new GetCommand({
                    TableName: 'testimony-users',
                    Key: { email: testimony.userEmail }
                }));
                return {
                    ...testimony,
                    authorName: userResult.Item?.name || 'Anonymous'
                };
            } catch {
                return {
                    ...testimony,
                    authorName: 'Anonymous'
                };
            }
        })
    );
    
    return { 
        statusCode: 200,
        headers: {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Methods': 'GET,OPTIONS'
        },
        body: JSON.stringify({ testimonies: testimoniesWithNames }) 
    };
}

async function updateTestimonyVisibility(data) {
    const { testimonyId, userEmail, isPublic } = data;
    
    await dynamodb.send(new UpdateCommand({
        TableName: 'testimonies',
        Key: { testimonyId },
        UpdateExpression: 'SET isPublic = :isPublic',
        ConditionExpression: 'userEmail = :userEmail',
        ExpressionAttributeValues: { 
            ':isPublic': isPublic,
            ':userEmail': userEmail
        }
    }));
    
    return { 
        statusCode: 200,
        headers: {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Methods': 'PUT,OPTIONS'
        },
        body: JSON.stringify({ message: 'Visibility updated successfully' }) 
    };
}

async function shareTestimony(data) {
    const { testimonyId, recipientEmail, senderName } = data;
    
    // Increment share count
    await dynamodb.send(new UpdateCommand({
        TableName: 'testimonies',
        Key: { testimonyId },
        UpdateExpression: 'ADD sharedCount :inc',
        ExpressionAttributeValues: { ':inc': 1 }
    }));
    
    // TODO: Trigger SES email function
    
    return { 
        statusCode: 200,
        headers: {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Methods': 'POST,OPTIONS'
        },
        body: JSON.stringify({ message: 'Testimony shared successfully' }) 
    };
}

// Share testimony with friend function
async function shareTestimonyWithFriend(data) {
    const { testimonyId, sharerName, friendEmail, shareMessage } = data;
    
    if (!testimonyId || !sharerName || !friendEmail) {
        return {
            statusCode: 400,
            headers: {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'POST,OPTIONS'
            },
            body: JSON.stringify({ error: 'Missing required fields' })
        };
    }
    
    // Get testimony details
    const testimonyResult = await dynamodb.send(new GetCommand({
        TableName: 'testimonies',
        Key: { testimonyId }
    }));
    
    if (!testimonyResult.Item || !testimonyResult.Item.isPublic) {
        return {
            statusCode: 404,
            headers: {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'POST,OPTIONS'
            },
            body: JSON.stringify({ error: 'Testimony not found' })
        };
    }
    
    // Increment share count
    await dynamodb.send(new UpdateCommand({
        TableName: 'testimonies',
        Key: { testimonyId },
        UpdateExpression: 'ADD sharedCount :inc',
        ExpressionAttributeValues: { ':inc': 1 }
    }));
    
    // TODO: Send email via SES
    // For now, just return success
    
    return {
        statusCode: 200,
        headers: {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Methods': 'POST,OPTIONS'
        },
        body: JSON.stringify({ message: 'Testimony shared successfully' })
    };
}

// Content moderation function with context awareness
async function moderateContent(title, content) {
    const combinedText = `${title} ${content}`.toLowerCase();
    
    // Check for required Christian content first
    const christianKeywords = [
        /\b(jesus|christ|god|lord|savior|salvation|faith|prayer|bible|christian|delivered|saved|redeemed|transformed)\b/i
    ];
    
    const hasChristianContent = christianKeywords.some(pattern => pattern.test(combinedText));
    if (!hasChristianContent) {
        return {
            approved: false,
            reason: 'Content does not appear to be a Christian testimony'
        };
    }
    
    // Context-aware patterns - look for redemption/transformation context
    const redemptionContext = [
        // Direct deliverance terms
        /\b(delivered from|saved from|freed from|rescued from|liberated from|released from|escaped from)\b/i,
        /\b(overcame|conquered|defeated|victory over|triumph over|breakthrough|breakthrough from)\b/i,
        /\b(god helped|jesus rescued|christ delivered|lord saved|holy spirit freed)\b/i,
        
        // Transformation language
        /\b(transformed|changed my life|renewed|restored|redeemed|regenerated|revived)\b/i,
        /\b(set free|made new|became new|new creation|new person|different person)\b/i,
        /\b(healed|healing|wholeness|restoration|recovery|recovered)\b/i,
        
        // Past vs present indicators
        /\b(used to|former|formerly|past|previous|old self|old me|old ways)\b/i,
        /\b(before jesus|before christ|before god|before salvation|pre-christian)\b/i,
        /\b(old life|new life|born again|rebirth|second chance|fresh start)\b/i,
        
        // Spiritual journey terms
        /\b(testimony|witness|miracle|blessing|grace|mercy|forgiveness)\b/i,
        /\b(repented|repentance|turned from|walked away from|left behind)\b/i,
        /\b(surrendered|gave up|quit|stopped|abandoned|forsook)\b/i,
        
        // God's intervention
        /\b(god intervened|divine intervention|god stepped in|jesus came|holy spirit moved)\b/i,
        /\b(answered prayer|god's plan|his will|divine purpose|calling|ministry)\b/i,
        /\b(blessed|favor|providence|guidance|led me|directed me)\b/i,
        
        // Emotional/spiritual states
        /\b(peace|joy|hope|love|faith|trust|strength|courage)\b/i,
        /\b(no longer|not anymore|never again|behind me|in the past)\b/i,
        /\b(now I|today I|currently|present|these days|nowadays)\b/i,
        
        // Church/community context
        /\b(church|pastor|ministry|fellowship|christian|believer|disciple)\b/i,
        /\b(baptized|baptism|altar call|accepted christ|received jesus)\b/i,
        /\b(bible study|prayer|worship|serve|serving god|mission)\b/i
    ];
    
    const hasRedemptionContext = redemptionContext.some(pattern => pattern.test(combinedText));
    
    // Harmful content patterns - but check context
    const potentiallyHarmful = [
        { pattern: /\b(suicide|kill myself|end my life)\b/i, type: 'suicide' },
        { pattern: /\b(drug dealer|selling drugs|trafficking)\b/i, type: 'drugs' },
        { pattern: /\b(addiction|alcoholic|drunk)\b/i, type: 'addiction' },
        { pattern: /\b(prostitution|sex work)\b/i, type: 'sexual' },
        { pattern: /\b(violence|fighting|anger)\b/i, type: 'violence' }
    ];
    
    // Check each potentially harmful pattern
    for (const item of potentiallyHarmful) {
        if (item.pattern.test(combinedText)) {
            // If harmful content found, check if it's in redemption context
            if (hasRedemptionContext) {
                // Allow if it's clearly a testimony about overcoming
                continue;
            } else {
                return {
                    approved: false,
                    reason: `Content contains ${item.type} references without clear redemption context`
                };
            }
        }
    }
    
    // Strict blocking patterns (no context exceptions)
    const alwaysBlock = [
        // Non-Christian religious promotion
        /\b(allah is|muhammad is|follow buddha|hindu god|islamic faith)\b/i,
        // Profanity
        /\b(fuck|shit|bitch|damn you|go to hell)\b/i,
        // Spam/Commercial
        /\b(buy now|click here|free money|lottery winner|business opportunity)\b/i,
        // Promoting harmful activities
        /\b(how to commit|join me in|let's do drugs|drinking party)\b/i
    ];
    
    for (const pattern of alwaysBlock) {
        if (pattern.test(combinedText)) {
            return {
                approved: false,
                reason: `Content contains prohibited material: ${pattern.source}`
            };
        }
    }
    
    return { approved: true };
}

// Flag user account for review
async function flagUserAccount(userEmail, reason, content) {
    const flagId = generateId();
    
    await dynamodb.send(new PutCommand({
        TableName: 'user-flags',
        Item: {
            flagId,
            userEmail,
            reason,
            content,
            status: 'pending',
            flaggedAt: new Date().toISOString()
        }
    }));
    
    // Update user account status
    await dynamodb.send(new UpdateCommand({
        TableName: 'testimony-users',
        Key: { email: userEmail },
        UpdateExpression: 'SET accountStatus = :status, flaggedAt = :flaggedAt',
        ExpressionAttributeValues: {
            ':status': 'flagged',
            ':flaggedAt': new Date().toISOString()
        }
    }));
}