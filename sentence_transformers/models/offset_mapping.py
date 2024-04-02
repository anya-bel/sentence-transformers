def create_offset_mapping(sentences, tokenized, tokenizer):
                offsets = []
                for num, sentence in enumerate(sentences):
                    s_counter = 0
                    o_counter = 0
                    offset = []
                    tokenized_sentence = tokenized.input_ids[num]
                    tokenized_tokens = [tokenizer.decode(x) for x in tokenized_sentence]
                    for elem in tokenized_tokens:
                        if elem in ['<s>', '</s>', '<pad>']:
                            offset.append((0,0,))
                            continue

                        br = []
                        if elem == '<unk>':
                            br.append(s_counter)
                            s_counter += 1
                        if s_counter > len(sentence)-1:
                            offset.append(br)
                            continue
                        elem_pos = 0
                        while elem_pos < len(elem) and sentence[s_counter] == elem[elem_pos] and s_counter <= len(sentence) :
                            br.append(s_counter)
                            s_counter += 1
                            o_counter += 1
                            elem_pos += 1
                            if s_counter > len(sentence)-1:
                                break
                        if s_counter < len(sentence)-1 and sentence[s_counter] in [' ', '\u2005', '\u2008', '\u2009', '\u200a', '\u202f', '\xa0']:
                            br.append(s_counter)
                            s_counter += 1
                        else:
                            if s_counter < len(sentence)-1 and sentence[s_counter+1] not in [' ', '\u2005', '\u2008', '\u2009', '\u200a', '\u202f', '\xa0']:
                                br.append(s_counter)
                            elif s_counter == len(sentence)-1:
                                br.append(s_counter)
                        if s_counter == len(sentence):
                            br.append(s_counter)
                        if len(br) == 1:
                            br.append(s_counter)
                        offset.append(br)
                    try:
                        offset_mapping = [(x[0], x[-1]) for x in offset]
                    except:
                        print(offset, s_counter)
                    offsets.append(offset_mapping)
                offsets = torch.tensor(offsets, dtype=torch.long)
                return offsets