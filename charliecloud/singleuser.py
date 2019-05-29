import subprocess
import os
import argparse

def extract_image(image_path, container_root_dir):
    os.makedirs(container_root_dir, exist_ok=True)
    extract_cmd = ['ch-tar2dir', image_path, container_root_dir]
    print(extract_cmd)
    proc = subprocess.run(
        extract_cmd,
        check=True
     )

    child_dirs = os.listdir(container_root_dir)
    assert len(child_dirs) == 1
    extracted_dir = os.path.join(container_root_dir, child_dirs[0])

    for p in os.listdir(extracted_dir):
        src_path = os.path.join(extracted_dir, p)
        target_path = os.path.join(container_root_dir, p)
        print(src_path, target_path)
        os.rename(src_path, target_path)

    os.rmdir(extracted_dir)

def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        'image_path'
    )
    argparser.add_argument(
        'container_path'
    )
    argparser.add_argument(
        'command',
        nargs=argparse.REMAINDER
    )

    args = argparser.parse_args()

    if not os.path.exists(args.container_path):
        extract_image(args.image_path, args.container_path)

    cmd = [
            'ch-run', args.container_path,
            '--set-env', os.path.join(args.container_path, 'environment'),
            # Notebook expects /run to be writeable, not readonly
            '--bind', '{}:/run'.format(os.path.join(args.container_path, 'run')),
            '--'
    ] + args.command
    print(' '.join(cmd), flush=True)
    os.execvp(cmd[0], cmd)

if __name__ == '__main__':
    main()