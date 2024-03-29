select count(ds.title), ds.title, ds.created_at
from delab_moderationrating mr
    join delab_moderationcandidate2 d on mr.mod_candidate_id = d.id
    join delab_tweet dt on dt.id = d.tweet_id
    join delab_simplerequest ds on dt.simple_request_id = ds.id
where mr.u_moderating_part is not null
  and mr.u_moderating_part <> ''
group by
    ds.title, ds.created_at
order by count(ds.title) desc;


select ds.created_at, ds.title, mr.u_mod_rating, mr.mod_coder_id
from delab_moderationrating mr
    join delab_moderationcandidate2 d on mr.mod_candidate_id = d.id
    join delab_tweet dt on dt.id = d.tweet_id
    join delab_simplerequest ds on dt.simple_request_id = ds.id
where mr.u_moderating_part is not null
  and mr.u_moderating_part <> ''
  and mr.u_mod_rating <> 0;

(select count(d.id) as metocode from delab_moderationcandidate2 d
where d.id not in (Select mod_candidate_id from delab_moderationrating where mod_coder_id = 1)
    and d.id not in (Select mod_candidate_id from delab_moderationrating where mod_coder_id <> 1))
union
(select count(d2.id) themtocode from delab_moderationcandidate2 d2
where d2.id not in (Select mod_candidate_id from delab_moderationrating where mod_coder_id <> 1)
    and d2.id in (Select mod_candidate_id from delab_moderationrating where mod_coder_id = 1));


select count(*) from delab_moderationrating;