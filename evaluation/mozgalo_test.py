import sys

import numpy as np

# Order of labels must be the same as the order in the list of test files, one per line.
# The labels should only be 0 or 1, if the file is not-packed or packed.
# Ex.
# 0
# 1
# 0
# ...

preds = np.array([int(line) for line in open(sys.argv[1], 'r')])
# Ground truth has the format with one entry per line, in the same order as the list of files in test set.
# each line has the format: is_packed,packer_group,is_held_out
# Ex.
# 0,0,0
# 1,2,0
# 1,1,1
# ...
gt = np.array([list(map(int, line.split(','))) for line in open(sys.argv[2], 'r')])

# Make sure your number of labels matches the number of files in test set
assert preds.shape[0] == gt.shape[0]

accuracy = (preds == gt[:, 0]).sum() / preds.shape[0]


# The number of points for total accuracy depends on the most accurate submitted solution
print('Accuracy: {}\n'.format(accuracy))

# Recall scores for dataset subgroups
notpacked = (gt[:, 1] == 0)
notpacked_recall = (preds[notpacked] == 0).sum() / notpacked.sum()
print('Notpacked recall: {} %'.format(notpacked_recall * 100))
packed_1or2 = ((gt[:, 1] == 1) | (gt[:, 1] == 2))
packed_1or2_recall = (preds[packed_1or2] == 1).sum() / packed_1or2.sum()
print('Overlay and Crypters recall: {} %'.format(packed_1or2_recall * 100))
packed_3 = (gt[:, 1] == 3)
packed_3_recall = (preds[packed_3] == 1).sum() / packed_3.sum()
print('Compressing packers recall: {} %'.format(packed_3_recall * 100))
packed_4 = (gt[:, 1] == 4)
packed_4_recall = (preds[packed_4] == 1).sum() / packed_4.sum()
print('Protectors recall: {} %'.format(packed_4_recall * 100))
print('Recall quality points: {}'.format(8 * np.prod([notpacked_recall,
                                                      notpacked_recall,
                                                      notpacked_recall,
                                                      packed_1or2_recall,
                                                      packed_3_recall,
                                                      packed_4_recall])))

# Held out packers recall
held_out = (gt[:, 2] == 1)
held_out_recall = (preds[held_out] == 1).sum() / held_out.sum()
print('Held out packers recall: {} %'.format(held_out_recall * 100))
print('Held out quality points: {} '.format(2 * held_out_recall))
