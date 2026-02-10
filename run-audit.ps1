# Run election data audit
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "RUNNING ELECTION DATA AUDIT" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

python audit_all_states_data.py

Write-Host "`n========================================" -ForegroundColor Green
Write-Host "AUDIT COMPLETE" -ForegroundColor Green
Write-Host "========================================`n" -ForegroundColor Green

Write-Host "To fix all discrepancies, run:" -ForegroundColor Yellow
Write-Host "  python fix_all_summary_guides.py`n" -ForegroundColor Yellow
