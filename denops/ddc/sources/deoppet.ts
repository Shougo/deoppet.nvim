import { BaseSource } from "../base/source.ts";
import { Candidate } from "../types.ts";
import { Denops } from "../deps.ts";

export class Source extends BaseSource {
  async gatherCandidates(denops: Denops): Promise<Candidate[]> {
    return [];
  }
}
