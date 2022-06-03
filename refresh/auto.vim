augroup refresh_browser
    autocmd!
    autocmd! TextChanged,InsertLeave */resume/resume/* :w %
augroup END
