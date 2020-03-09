from typing import Dict, List
from index.IndexEntriesGroup import IndexEntriesGroup


class CloneDetector:

    def __init__(self, clone_index):
        self.clone_index = clone_index
        self.origin_file_name = '' # FIXME: dynamically

    def detect_clones(self, index_entries):
        """
        Detects and reports the clones resulting by the comparison of the passed index_entries
        and the entries of the existing clone index

        Args:
            index_entries: index entries of the file to be checked against the existing clone
            index. Corresponds to "f" in the original paper
        """
        same_hash_block_groups: List[IndexEntriesGroup] = self.create_groups(index_entries)

        for i in range(1, len(same_hash_block_groups)):
            prev_entries_group: IndexEntriesGroup = same_hash_block_groups[i-1]
            current_entries_group: IndexEntriesGroup = same_hash_block_groups[i]

            if current_entries_group.get__size() < 2 or current_entries_group.subset_of(prev_entries_group, 1):
                continue

            active_set: IndexEntriesGroup = current_entries_group

            for j in range(i + 1, len(same_hash_block_groups)):
                intersection_group: IndexEntriesGroup = active_set.intersect(same_hash_block_groups[j])
                if intersection_group.get__size() < active_set.get__size():
                    print("REPORTING CLONES")
                active_set = intersection_group
                if active_set.get__size() < 2 or active_set.subset_of(same_hash_block_groups[i - 1], j - i + 1):
                    break

    def create_groups(self, index_entries):
        groups_by_hash: Dict[str, IndexEntriesGroup] = {}

        # hash -> index_entry dictionary based on the passed index_entries
        for entry in index_entries:
            groups_by_hash.setdefault(entry.get__sequence_hash(), IndexEntriesGroup()).add_entry(entry)

        clone_index_entries_by_hash = self.clone_index.get__index_entries_by_hash()
        # extends the "groups_by_hash" based on the entries of the clone index
        for hash_val in groups_by_hash.keys():
            # check if the hash value exists in the clone index (a.k.a if there is a clone)
            clone_index_entries = clone_index_entries_by_hash.get(hash_val)

            if clone_index_entries is not None:
                group = groups_by_hash.get(hash_val)
                for clone_index_entry in clone_index_entries:
                    if clone_index_entry.get__file_name != self.origin_file_name:
                        group.add_entry(clone_index_entry)

                list.sort(group.get__index_entries_group(), key=lambda entry: (entry.get__file_name(), entry.get__statement_index()))

        # TODO: For debugging, remove later
        for hash_key in groups_by_hash.keys():
            print("For hash key \"" + hash_key + "\"")
            print(groups_by_hash[hash_key])

        f_size = len(index_entries)
        same_hash_block_groups: List[IndexEntriesGroup] = [None] * (f_size + 2)

        same_hash_block_groups[0] = IndexEntriesGroup()  # i=0 will be empty
        for entry in index_entries:
            hash_value = entry.get__sequence_hash()
            index = entry.get__statement_index() + 1
            same_hash_block_groups[index] = groups_by_hash.get(hash_value)

        same_hash_block_groups[f_size+1] = IndexEntriesGroup()  # i=len+1 will be empty

        return same_hash_block_groups
