$ErrorActionPreference = 'Continue'
Get-ScheduledTask | ForEach-Object {
    $task = $_
    foreach ($a in $task.Actions) {
        [pscustomobject]@{
            TaskPath=$task.TaskPath; TaskName=$task.TaskName; State=$task.State
            RunAs=$task.Principal.UserId; RunLevel=$task.Principal.RunLevel
            Execute=$a.Execute; Arguments=$a.Arguments; WorkingDirectory=$a.WorkingDirectory
        }
    }
} | Sort-Object TaskPath,TaskName | Format-Table -AutoSize
