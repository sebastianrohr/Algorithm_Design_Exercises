@ECHO OFF
for %%f in (data\*.txt) do (
    echo %%~nf
    python red_scare_solution.py < "data\%%~nf.txt"
)