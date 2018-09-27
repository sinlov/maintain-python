package com.shishike.mobile.module.inventory.test;


import android.os.Bundle;
import android.support.v4.app.FragmentActivity;
import android.widget.CheckBox;
import android.widget.FrameLayout;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.RelativeLayout;
import android.widget.TextView;

import com.keruyun.mobile.inventory.management.ui.R;

import butterknife.BindView;
import butterknife.ButterKnife;

public class ButterknifeTest extends FragmentActivity {

        ImageView mTitleBackImg;
        RelativeLayout mTitleBackLayout;
        TextView mTitleCenterTv;
        CheckBox mTitleCenterSpinnerIndicator;
        LinearLayout mTitleCenterLayout;
        TextView mTitleRightTv;
        TextView mTitleRightImv;
        LinearLayout mSearchView;
        TextView mApplyNoTv;
        ImageView mApplyNoDetailOpen;
        TextView mApplyDateLabelTv;
        TextView mApplyDateTv;
        RelativeLayout mApplyDateLayout;
        TextView mArriveDateLabelTv;
        TextView mArriveDateTv;
        ImageView mApplyNoDetailHide;
        RelativeLayout mArriveDateLayout;
        TextView mRefuseReasonLabelTv;
        TextView mRefuseReasonTv;
        RelativeLayout mRefuseLayout;
        LinearLayout mApplyNoPanel;
        TextView mUpdateName;
        TextView mUpdateTime;
        RelativeLayout mApplyedInfoLayout;
        TextView mBottomBarCommand;
        TextView mBottomBarAutoAdd;
        TextView mTotalPriceTv;
        TextView mTotalTypeAll;
        FrameLayout mflShowCost;
        ImageView mShaoMaView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_distribution_template);

        mTitleBackImg = (ImageView) findViewById(R.id.title_backImg);
        mTitleBackLayout = (RelativeLayout) findViewById(R.id.title_back_layout);
        mTitleCenterTv = (TextView) findViewById(R.id.title_center_tv);
        mTitleCenterSpinnerIndicator = (CheckBox) findViewById(R.id.title_center_spinner_indicator);
        mTitleCenterLayout = (LinearLayout) findViewById(R.id.title_center_layout);
        mTitleRightTv = (TextView) findViewById(R.id.title_right_tv);
        mTitleRightImv = (TextView) findViewById(R.id.title_right_imv);
        mSearchView = (LinearLayout) findViewById(R.id.search_panel_layout);
        mApplyNoTv = (TextView) findViewById(R.id.apply_no_tv);
        mApplyNoDetailOpen = (ImageView) findViewById(R.id.apply_no_detail_open);
        mApplyDateLabelTv = (TextView) findViewById(R.id.apply_date_label_tv);
        mApplyDateTv = (TextView) findViewById(R.id.apply_date_tv);
        mApplyDateLayout = (RelativeLayout) findViewById(R.id.apply_date_layout);
        mArriveDateLabelTv = (TextView) findViewById(R.id.arrive_date_label_tv);
        mArriveDateTv = (TextView) findViewById(R.id.arrive_date_tv);
        mApplyNoDetailHide = (ImageView) findViewById(R.id.apply_no_detail_hide);
        mArriveDateLayout = (RelativeLayout) findViewById(R.id.arrive_date_layout);
        mRefuseReasonLabelTv = (TextView) findViewById(R.id.refuse_reason_label_tv);
        mRefuseReasonTv = (TextView) findViewById(R.id.refuse_reason_tv);
        mRefuseLayout = (RelativeLayout) findViewById(R.id.refuse_layout);
        mApplyNoPanel = (LinearLayout) findViewById(R.id.apply_no_panel);
        mUpdateName = (TextView) findViewById(R.id.update_name);
        mUpdateTime = (TextView) findViewById(R.id.update_time);
        mApplyedInfoLayout = (RelativeLayout) findViewById(R.id.applyed_info_layout);
        mBottomBarCommand = (TextView) findViewById(R.id.bottom_bar_command);
        mBottomBarAutoAdd = (TextView) findViewById(R.id.bottom_bar_auto_add);
        mTotalPriceTv = (TextView) findViewById(R.id.total_price_tv);
        mTotalTypeAll = (TextView) findViewById(R.id.price_division);
        mflShowCost = (FrameLayout) findViewById(R.id.delivery_fl_cost_show);
        mShaoMaView = (ImageView) findViewById(R.id.iv_inventory_shaomao_press);

    }
}