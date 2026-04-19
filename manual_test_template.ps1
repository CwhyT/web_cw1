# ShelfSense API manual test template
# Usage:
# 1. Start the API server first:
#    uvicorn app.main:app --reload
# 2. Run this script in another PowerShell window:
#    .\manual_test_template.ps1

$baseUrl = "http://127.0.0.1:8000"
$suffix = Get-Date -Format "yyyyMMddHHmmss"

Write-Host "Testing ShelfSense API at $baseUrl" -ForegroundColor Cyan

# 1. Health check
$health = Invoke-RestMethod -Method Get -Uri "$baseUrl/health"
Write-Host "Health:" ($health | ConvertTo-Json -Compress)

# 2. Register user
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
$me = Invoke-RestMethod -Method Get -Uri "$baseUrl/api/auth/me" -Headers $headers
Write-Host "Current user:" ($me | ConvertTo-Json -Compress)

# 5. Search books
$search = Invoke-RestMethod -Method Get -Uri "$baseUrl/api/books/search?q=python&limit=3"
Write-Host "Book search result count:" $search.results.Count

# 6. Optional book detail lookup
$bookDetail = Invoke-RestMethod -Method Get -Uri "$baseUrl/api/books/OL45804W"
Write-Host "Book detail title:" $bookDetail.title

# 7. Create reading list
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
$allLists = Invoke-RestMethod -Method Get -Uri "$baseUrl/api/lists" -Headers $headers
Write-Host "Reading list count:" $allLists.Count

# 9. Add book to reading list
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
$itemUpdateBody = @{ status = "finished" } | ConvertTo-Json
$updatedItem = Invoke-RestMethod `
    -Method Put `
    -Uri "$baseUrl/api/lists/$($list.id)/items/$($item.id)" `
    -Headers $headers `
    -ContentType "application/json" `
    -Body $itemUpdateBody

Write-Host "Updated list item status:" $updatedItem.status

# 11. Create review
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
$savedReview = Invoke-RestMethod -Method Get -Uri "$baseUrl/api/reviews/$($review.id)"
Write-Host "Saved review rating:" $savedReview.rating

# 13. Update review
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
$bookReviews = Invoke-RestMethod -Method Get -Uri "$baseUrl/api/reviews/book/$bookId"
Write-Host "Review count for book:" $bookReviews.Count

# 15. Analytics
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
# Uncomment these if you want to remove test data after checking results.
#
# Invoke-RestMethod -Method Delete -Uri "$baseUrl/api/reviews/$($review.id)" -Headers $headers
# Invoke-RestMethod -Method Delete -Uri "$baseUrl/api/lists/$($list.id)/items/$($item.id)" -Headers $headers
# Invoke-RestMethod -Method Delete -Uri "$baseUrl/api/lists/$($list.id)" -Headers $headers

Write-Host "Manual test flow completed." -ForegroundColor Green
