import os
import sys
import shutil
from pathlib import Path

def get_browser_cache_paths():
    """
    Returns OS-aware target directories for standard Google Chrome caches
    across Windows, macOS, and Linux.
    """
    home = Path.home()
    paths = []
    
    if sys.platform == "win32":
        # Windows OS Chrome targets
        local_app_data = os.getenv("LOCALAPPDATA")
        if local_app_data:
            paths.append(Path(local_app_data) / "Google" / "Chrome" / "User Data" / "Default" / "Cache" / "Cache_Data")
            paths.append(Path(local_app_data) / "Microsoft" / "Edge" / "User Data" / "Default" / "Cache" / "Cache_Data")
    elif sys.platform == "darwin":
        # macOS targets
        paths.append(home / "Library" / "Caches" / "Google" / "Chrome" / "Default" / "Cache")
    else:
        # Linux / Unix targets
        paths.append(home / ".cache" / "google-chrome" / "Default" / "Cache")
        
    return paths

def run_browser_cache_cleaner():
    """
    OS-aware helper that attempts to clear targeted browser cache folders.
    Degrades gracefully with complete user explanations on permission issues.
    """
    os_name = sys.platform
    target_paths = get_browser_cache_paths()
    
    if not target_paths:
        return f"Browser Agent: Platform '{os_name}' has no standard Chrome/Edge cache adapters defined."

    cleaned_folders = []
    failed_folders = []

    for path in target_paths:
        resolved_path = path.expanduser().resolve()
        if not resolved_path.exists():
            continue
            
        try:
            # Clear contents safely by deleting files inside
            for item in resolved_path.iterdir():
                if item.is_file() or item.is_symlink():
                    item.unlink()
                elif item.is_dir():
                    shutil.rmtree(item)
            cleaned_folders.append(str(resolved_path))
        except PermissionError:
            failed_folders.append(f"{resolved_path} (Access Denied - browser may be running or lock is active)")
        except Exception as e:
            failed_folders.append(f"{resolved_path} (Error: {e})")

    # Construct user reply
    if not cleaned_folders and not failed_folders:
        return f"Browser Agent: No active Chrome or Edge cache folders found in default paths for '{os_name}'."
        
    result_msg = f"Browser Agent Maintenance Run on '{os_name}':\n"
    if cleaned_folders:
        result_msg += "Successfully cleared cache files in:\n" + "\n".join([f"- {f}" for f in cleaned_folders]) + "\n"
    if failed_folders:
        result_msg += "Could not clean the following paths (gracefully skipped):\n" + "\n".join([f"- {f}" for f in failed_folders])
        
    return result_msg
