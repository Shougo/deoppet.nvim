import {
  BaseSource,
  Candidate,
} from "https://deno.land/x/ddc_vim@v0.0.1/base/source.ts";
import { Denops } from "https://deno.land/x/ddc_vim@v0.0.1/base/deps.ts";

export class Source extends BaseSource {
  async gatherCandidates(denops: Denops): Promise<Candidate[]> {
    return [];
  }
}
