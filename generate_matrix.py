#!/usr/bin/python3

from glob import glob


def main(arg):
    filelist = glob('*{}.csv'.format(arg))
    filelist.sort()
    treeko_dict = dict()

    for table in filelist:
        with open(table, 'r') as raw:
            treeko = dict()
            for line in raw:
                line_split = line.strip().split('\t')
                treeko[line_split[0]] = line_split[3]
            # ensure same order
            treeko_dict[table.split('-')[0]] = treeko

    print(treeko_dict['rbcL.tree']['accD.tree'])
    print(treeko_dict['accD.tree']['rbcL.tree'])
    bmin50_filelist = [i.split('-')[0] for i in filelist]
    with open('{}_matrix.tsv'.format(arg), 'w') as out:
        out.write('Name\t')
        out.write('\t'.join(bmin50_filelist))
        out.write('\n')
        for i in bmin50_filelist:
            line = i + '\t'
            for j in bmin50_filelist:
                if treeko_dict[i][i] != '0.0':
                    raise Exception
                line += (treeko_dict[i][j]+'\t')
            line += '\n'
            out.write(line)


if __name__ == '__main__':
    main('bmin50')
    main('bmin0')
