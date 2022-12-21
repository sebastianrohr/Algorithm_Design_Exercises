@ECHO OFF
for %%f in (*.txt) do (
    echo %%~nf
    python red_scare_solution.py < "%%~nf.txt"
)