# ShelfSense API manual test template
#
# This script is a reusable manual test flow for the main project features.
# It is designed for quick end-to-end checking without typing every command by hand.
#
# What this script covers:
# - server health check
# - user registration
# - user login and token retrieval
# - current-user lookup
# - book search and book detail lookup
# - reading list creation and item management
# - review creation and update
# - analytics and recommendation endpoints
#
# Usage:
# 1. Start the API server first:
#    uvicorn app.main:app --reload
# 2. Run this script in another PowerShell window:
#    .\manual_test_template.ps1
#
# Notes:
# - The script creates a unique user each time using a timestamp suffix.
# - This avoids "username or email already exists" conflicts across repeated runs.
# - The script prints short summaries instead of dumping every full response.
# - At the bottom there are optional cleanup commands you can uncomment if needed.

# Base API address for local testing.
# Change this if you later deploy the project and want to test a hosted version.
$baseUrl = "http://127.0.0.1:8000"

# Use the current timestamp to generate unique usernames and email addresses.
# This keeps the script reusable even if you run it many times.
$suffix = Get-Date -Format "yyyyMMddHHmmss"

Write-Host "Testing ShelfSense API at $baseUrl" -ForegroundColor Cyan

# 1. Health check
# Purpose:
# - confirm that the FastAPI application is running
# - verify that the server can respond before we test business endpoints
$health = Invoke-RestMethod -Method Get -Uri "$baseUrl/health"
Write-Host "Health:" ($health | ConvertTo-Json -Compress)

# 2. Register user
# Purpose:
# - create a fresh user account for this test run
# - store the returned user object for later steps
# You can change the password here if you want to test other credentials.
$registerBody = @{
    username = "tester_$suffix"
    email = "tester_$suffix@example.com"
    password = "secret123"
} | ConvertTo-Json

$user = Invoke-RestMethod `
    -Method Post `
    -Uri "$baseUrl/api/auth/register" `
    -ContentType "application/json" `
    -Body $registerBody

Write-Host "Registered user id:" $user.id

# 3. Login
# Purpose:
# - exchange the email/password for a bearer token
# - save the token into $headers so protected endpoints can be called later
$loginBody = @{
    email = $user.email
    password = "secret123"
} | ConvertTo-Json

$login = Invoke-RestMethod `
    -Method Post `
    -Uri "$baseUrl/api/auth/login" `
    -ContentType "application/json" `
    -Body $loginBody

$token = $login.access_token
$headers = @{ Authorization = "Bearer $token" }

Write-Host "Login succeeded. Token received." -ForegroundColor Green

# 4. Current user
# Purpose:
# - confirm that the token works
# - verify that the API can identify the logged-in user correctly
$me = Invoke-RestMethod -Method Get -Uri "$baseUrl/api/auth/me" -Headers $headers
Write-Host "Current user:" ($me | ConvertTo-Json -Compress)

# 5. Search books
# Purpose:
# - test the Open Library search integration
# - confirm that the API returns a JSON result list
# You can replace "python" with another keyword if you want.
$search = Invoke-RestMethod -Method Get -Uri "$baseUrl/api/books/search?q=python&limit=3"
Write-Host "Book search result count:" $search.results.Count

# 6. Optional book detail lookup
# Purpose:
# - test the detailed book endpoint
# - verify that a known Open Library work key can be resolved
# The key OL45804W is just a simple example; you can swap it for another one.
$bookDetail = Invoke-RestMethod -Method Get -Uri "$baseUrl/api/books/OL45804W"
Write-Host "Book detail title:" $bookDetail.title

# 7. Create reading list
# Purpose:
# - create a reading list owned by the logged-in user
# - verify that protected POST endpoints work with bearer authentication
$listBody = @{
    user_id = $user.id
    name = "Manual Test List"
    description = "Created from manual_test_template.ps1"
} | ConvertTo-Json

$list = Invoke-RestMethod `
    -Method Post `
    -Uri "$baseUrl/api/lists" `
    -Headers $headers `
    -ContentType "application/json" `
    -Body $listBody

Write-Host "Created list id:" $list.id

# 8. List reading lists
# Purpose:
# - confirm that the new list is visible when fetching the user's lists
$allLists = Invoke-RestMethod -Method Get -Uri "$baseUrl/api/lists" -Headers $headers
Write-Host "Reading list count:" $allLists.Count

# 9. Add book to reading list
# Purpose:
# - add a book into the reading list
# - verify that the API can also cache the book locally in the database
# You can replace this payload with another book if you want to test different data.
$itemBody = @{
    openlibrary_key = "/works/OL45804W"
    title = "Learning Python"
    author_name = "Mark Lutz"
    first_publish_year = 1999
    subject = "Python, Programming"
    cover_url = "https://covers.openlibrary.org/b/id/12345-L.jpg"
    status = "to_read"
} | ConvertTo-Json

$item = Invoke-RestMethod `
    -Method Post `
    -Uri "$baseUrl/api/lists/$($list.id)/items" `
    -Headers $headers `
    -ContentType "application/json" `
    -Body $itemBody

$bookId = $item.book_id
Write-Host "Added list item id:" $item.id "book id:" $bookId

# 10. Update list item status
# Purpose:
# - update the book's reading status inside the list
# - verify that item-level update endpoints work correctly
$itemUpdateBody = @{ status = "finished" } | ConvertTo-Json
$updatedItem = Invoke-RestMethod `
    -Method Put `
    -Uri "$baseUrl/api/lists/$($list.id)/items/$($item.id)" `
    -Headers $headers `
    -ContentType "application/json" `
    -Body $itemUpdateBody

Write-Host "Updated list item status:" $updatedItem.status

# 11. Create review
# Purpose:
# - create a review linked to the cached local book record
# - confirm that authenticated write access works for review endpoints
$reviewBody = @{
    user_id = $user.id
    book_id = $bookId
    rating = 5
    review_text = "Helpful and well structured."
} | ConvertTo-Json

$review = Invoke-RestMethod `
    -Method Post `
    -Uri "$baseUrl/api/reviews" `
    -Headers $headers `
    -ContentType "application/json" `
    -Body $reviewBody

Write-Host "Created review id:" $review.id

# 12. Get review
# Purpose:
# - fetch the saved review by id
# - verify that the review was stored correctly
$savedReview = Invoke-RestMethod -Method Get -Uri "$baseUrl/api/reviews/$($review.id)"
Write-Host "Saved review rating:" $savedReview.rating

# 13. Update review
# Purpose:
# - update the saved review text and rating
# - confirm that protected update works and the new values are persisted
$reviewUpdateBody = @{
    rating = 4
    review_text = "Still good, but slightly repetitive."
} | ConvertTo-Json

$updatedReview = Invoke-RestMethod `
    -Method Put `
    -Uri "$baseUrl/api/reviews/$($review.id)" `
    -Headers $headers `
    -ContentType "application/json" `
    -Body $reviewUpdateBody

Write-Host "Updated review rating:" $updatedReview.rating

# 14. Book reviews
# Purpose:
# - list all reviews that belong to the current cached book
# - confirm that the review appears in the book review collection
$bookReviews = Invoke-RestMethod -Method Get -Uri "$baseUrl/api/reviews/book/$bookId"
Write-Host "Review count for book:" $bookReviews.Count

# 15. Analytics
# Purpose:
# - test the analytics endpoints that rely on locally cached books and reviews
# - confirm that the user preference and recommendation logic has usable output
$genres = Invoke-RestMethod -Method Get -Uri "$baseUrl/api/analytics/genres"
Write-Host "Top genres count:" $genres.genres.Count

$preferences = Invoke-RestMethod `
    -Method Get `
    -Uri "$baseUrl/api/analytics/user/$($user.id)/preferences"
Write-Host "User preferences:" ($preferences | ConvertTo-Json -Compress)

$recommendations = Invoke-RestMethod `
    -Method Get `
    -Uri "$baseUrl/api/analytics/recommendations/user/$($user.id)"
Write-Host "Recommendation count:" $recommendations.recommendations.Count

# 16. Optional cleanup
# Purpose:
# - remove the review, list item, and list created by this script
# By default these are commented out so you can inspect the saved data afterwards.
# Uncomment them only if you want the script to clean up automatically after the test.
#
# Invoke-RestMethod -Method Delete -Uri "$baseUrl/api/reviews/$($review.id)" -Headers $headers
# Invoke-RestMethod -Method Delete -Uri "$baseUrl/api/lists/$($list.id)/items/$($item.id)" -Headers $headers
# Invoke-RestMethod -Method Delete -Uri "$baseUrl/api/lists/$($list.id)" -Headers $headers

Write-Host "Manual test flow completed." -ForegroundColor Green
